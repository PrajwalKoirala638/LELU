#!/usr/bin/env python3
"""Check and fix every .tsv file under this script's folder, never changing the originals."""  # Module description

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import codecs  # Incremental decoders and byte-order marks
import os  # Folder walking, path building, and file removal
import re  # Regular expressions for junk-character removal
from collections import Counter  # Counts how often each value appears
from dataclasses import dataclass  # Lets us declare a simple data class

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
ROOT_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))  # The folder this script lives in
INPUT_FILE_EXTENSION = ".tsv"  # Only files with this extension are processed
FIXED_FILE_SUFFIX = "_fixed.tsv"  # Cleaned output is saved as <name>_fixed.tsv
REJECTED_FILE_SUFFIX = "_rejects.tsv"  # Unfixable rows are saved as <name>_rejects.tsv
FIELD_SEPARATOR = "\t"  # TSV fields are separated by a tab
UTF16_BYTE_ORDER_MARKS = (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)  # Two-byte UTF-16 signatures
FALLBACK_ENCODINGS = ("utf-8-sig", "cp1252", "latin-1")  # Tried in this order when no UTF-16 mark
DECODE_CHUNK_SIZE_IN_BYTES = 1024 * 1024  # Read big files one megabyte at a time
MAXIMUM_DETAIL_LINES_PER_FILE = 10  # Limit on individual issues shown per file
JUNK_CHARACTER_PATTERN = re.compile(  # Control characters, replacement char, zero-width chars
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffd\u200b\ufeff]"  # The characters to strip
)  # End of pattern definition

BLANK_ROW_CATEGORY = "blank row removed"  # Issue label
REJOINED_ROW_CATEGORY = "split row rejoined (stray newline)"  # Issue label
WRONG_COLUMN_COUNT_CATEGORY = "wrong column count (moved to rejects)"  # Issue label
WHITESPACE_CATEGORY = "whitespace trimmed"  # Issue label
JUNK_CATEGORY = "junk characters removed"  # Issue label
UNBALANCED_QUOTE_CATEGORY = "unbalanced quote (kept, please review)"  # Issue label
DUPLICATE_CATEGORY = "duplicate row removed (includes repeated headers)"  # Issue label


# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------
@dataclass  # Generates __init__ and __repr__ automatically
class FileSummary:  # The final numbers for one processed file
    file_path: str  # Path of the original file
    encoding_name: str  # Encoding that was detected
    expected_column_count: int  # The normal number of columns
    rows_read: int  # Lines read from the original
    rows_kept: int  # Rows written to the fixed file
    rows_rejected: int  # Rows written to the rejects file
    total_issue_count: int  # Every problem found


class IssueLog:  # Counts every issue but remembers only a few details
    def __init__(self, maximum_detail_lines):  # Sets up an empty log
        self.maximum_detail_lines = maximum_detail_lines  # How many details to remember
        self.issue_counts = Counter()  # Number of issues per category
        self.detail_lines = []  # The first few detailed messages
        self.total_issue_count = 0  # Number of issues across all categories

    def record(self, line_number, category, detail=""):  # Registers one issue
        self.total_issue_count += 1  # Count it in the total
        self.issue_counts[category] += 1  # Count it in its category
        if len(self.detail_lines) < self.maximum_detail_lines:  # Still room for details
            self.detail_lines.append(f"line {line_number}: {category} {detail}".rstrip())  # Save


class PeekableRowStream:  # Wraps a row generator so the next row can be inspected
    def __init__(self, row_iterator):  # Sets up the stream
        self.row_iterator = row_iterator  # The underlying generator
        self.buffered_item = None  # The row looked at but not yet taken
        self.has_buffered_item = False  # Whether a row is waiting in the buffer

    def peek(self):  # Looks at the next row without consuming it
        if not self.has_buffered_item:  # Nothing buffered yet
            try:  # Ask the generator for one more row
                self.buffered_item = next(self.row_iterator)  # Buffer it
            except StopIteration:  # The file has no more rows
                return None  # Signal the end of the file
            self.has_buffered_item = True  # A row is now waiting
        return self.buffered_item  # Return the waiting row

    def take(self):  # Consumes and returns the next row
        next_item = self.peek()  # Make sure a row is buffered
        self.has_buffered_item = False  # The buffer is now empty
        return next_item  # Return the row that was taken


# ----------------------------------------------------------------------
# Finding files and naming outputs
# ----------------------------------------------------------------------
def find_tsv_file_paths(root_directory_path):  # Yields every original .tsv file under a folder
    for current_directory_path, directory_names, file_names in os.walk(root_directory_path):  # Walk
        directory_names.sort()  # Visit sub-folders in a stable order
        for file_name in sorted(file_names):  # Visit files in a stable order
            is_tsv_file = file_name.endswith(INPUT_FILE_EXTENSION)  # Must be a .tsv file
            is_generated_file = file_name.endswith((FIXED_FILE_SUFFIX, REJECTED_FILE_SUFFIX))  # Ours
            if is_tsv_file and not is_generated_file:  # Original data files only
                yield os.path.join(current_directory_path, file_name)  # Hand back the full path


def build_output_file_paths(input_file_path):  # Builds the two output paths for one input file
    path_without_extension = os.path.splitext(input_file_path)[0]  # Remove ".tsv"
    fixed_file_path = path_without_extension + FIXED_FILE_SUFFIX  # <name>_fixed.tsv
    rejected_file_path = path_without_extension + REJECTED_FILE_SUFFIX  # <name>_rejects.tsv
    assert input_file_path not in (fixed_file_path, rejected_file_path), "Never overwrite originals."
    return fixed_file_path, rejected_file_path  # Return both paths


# ----------------------------------------------------------------------
# Reading
# ----------------------------------------------------------------------
def can_decode_entire_file(file_path, encoding_name):  # Tests an encoding against the whole file
    decoder = codecs.getincrementaldecoder(encoding_name)()  # Decoder that accepts chunks
    try:  # Decoding may fail
        with open(file_path, "rb") as input_file:  # Open as raw bytes
            while True:  # Keep reading chunks
                chunk = input_file.read(DECODE_CHUNK_SIZE_IN_BYTES)  # Read one chunk
                if not chunk:  # End of file reached
                    break  # Stop reading
                decoder.decode(chunk)  # Raises an error when the bytes do not fit
            decoder.decode(b"", final=True)  # Flush any partial character at the end
    except UnicodeError:  # The encoding does not fit this file
        return False  # Report failure
    return True  # Every byte decoded successfully


def detect_file_encoding(file_path):  # Finds an encoding that can read the file
    with open(file_path, "rb") as input_file:  # Open as raw bytes
        first_two_bytes = input_file.read(2)  # Read the possible byte-order mark
    if first_two_bytes in UTF16_BYTE_ORDER_MARKS:  # The file announces UTF-16
        return "utf-16"  # Use UTF-16
    for encoding_name in FALLBACK_ENCODINGS:  # Try each fallback in turn
        if can_decode_entire_file(file_path, encoding_name):  # This one works
            return encoding_name  # Use it
    raise ValueError("Could not decode the file with any supported encoding.")  # Nothing worked


def generate_rows(file_path, encoding_name):  # Yields (line_number, fields) one row at a time
    with open(file_path, "r", encoding=encoding_name, newline=None) as input_file:  # Normalizes CRLF
        for line_number, line_text in enumerate(input_file, start=1):  # Number lines from 1
            yield line_number, line_text.rstrip("\n").split(FIELD_SEPARATOR)  # Split into fields


def is_blank_row(fields):  # True when every field in the row is empty
    return not any(field.strip() for field in fields)  # No field has visible content


def count_column_widths(file_path, encoding_name):  # Counts how many rows have each width
    width_counts = Counter()  # Maps width to number of rows
    for _, fields in generate_rows(file_path, encoding_name):  # Every row, ignoring line numbers
        if not is_blank_row(fields):  # Blank rows do not count
            width_counts[len(fields)] += 1  # Count this width
    return width_counts  # Return the tally


def determine_expected_column_count(width_counts):  # Picks the most common width
    if not width_counts:  # Every row was blank, or the file is empty
        raise ValueError("The file appears to be empty.")  # Nothing to analyze
    expected_column_count = width_counts.most_common(1)[0][0]  # The most common width
    assert expected_column_count > 0, "Expected column count must be positive."  # Sanity check
    return expected_column_count  # Return the winning width


# ----------------------------------------------------------------------
# Cleaning
# ----------------------------------------------------------------------
def remove_junk_characters(field):  # Strips control and invisible characters
    return JUNK_CHARACTER_PATTERN.sub("", field)  # Replace each junk character with nothing


def has_unbalanced_quote(field):  # True when a field has an odd number of quotes
    return field.count('"') % 2 == 1  # An odd count means a quote was never closed


def try_rejoin_split_row(current_fields, next_fields, expected_column_count):  # Repairs split rows
    merged_fields = (  # Join the last field of this row with the first of the next
        current_fields[:-1]  # All fields except the last of the current row
        + [current_fields[-1] + " " + next_fields[0]]  # The two halves of the split field
        + next_fields[1:]  # The remaining fields of the next row
    )  # End of merged row construction
    if len(merged_fields) == expected_column_count:  # The merge produced the right width
        return merged_fields  # The repair worked
    return None  # The repair did not work


def attempt_split_row_repair(fields, row_stream, expected_column_count, line_number, issue_log):
    next_item = row_stream.peek()  # Look at the following row without consuming it
    if next_item is None:  # There is no following row
        return fields, None  # Nothing to repair with
    next_line_number, next_fields = next_item  # Unpack the following row
    merged_fields = try_rejoin_split_row(fields, next_fields, expected_column_count)  # Try to merge
    if merged_fields is None:  # The merge did not give the right width
        return fields, None  # Leave the row as it is
    issue_log.record(line_number, REJOINED_ROW_CATEGORY)  # Log the repair
    row_stream.take()  # Consume the following row, since it was merged in
    return merged_fields, next_line_number  # Return the repaired row and the last line used


def clean_single_row(fields, line_number, issue_log):  # Cleans one row and logs what changed
    stripped_fields = [field.strip() for field in fields]  # Trim whitespace around each field
    if stripped_fields != fields:  # Something was trimmed
        issue_log.record(line_number, WHITESPACE_CATEGORY)  # Log it
    junk_free_fields = [remove_junk_characters(field) for field in stripped_fields]  # Strip junk
    if junk_free_fields != stripped_fields:  # Something was stripped
        issue_log.record(line_number, JUNK_CATEGORY)  # Log it
    for field in junk_free_fields:  # Look at each field
        if has_unbalanced_quote(field):  # A quote was left open
            issue_log.record(line_number, UNBALANCED_QUOTE_CATEGORY, repr(field[:30]))  # Log preview
            break  # One warning per row is enough
    return junk_free_fields  # Return the cleaned fields


def stream_and_clean_rows(input_file_path, encoding_name, expected_column_count,
                          fixed_file, rejected_file, issue_log):  # Core row-by-row loop
    row_stream = PeekableRowStream(generate_rows(input_file_path, encoding_name))  # Peekable rows
    seen_fingerprints = set()  # Compact memory of rows already kept
    rows_read = 0  # Highest line number consumed so far
    rows_kept = 0  # Rows written to the fixed file
    rows_rejected = 0  # Rows written to the rejects file
    while row_stream.peek() is not None:  # Continue until the file ends
        line_number, fields = row_stream.take()  # Consume the next row
        rows_read = line_number  # Remember how far we have read
        if is_blank_row(fields):  # The row has no content
            issue_log.record(line_number, BLANK_ROW_CATEGORY)  # Log it
            continue  # Skip to the next row
        if len(fields) < expected_column_count:  # The row is too short
            fields, last_line_used = attempt_split_row_repair(  # Try merging with the next row
                fields, row_stream, expected_column_count, line_number, issue_log  # Inputs
            )  # End of repair attempt
            if last_line_used is not None:  # A merge consumed another line
                rows_read = last_line_used  # Update how far we have read
        if len(fields) != expected_column_count:  # Still the wrong width
            detail = f"({len(fields)} columns, expected {expected_column_count})"  # Explain
            issue_log.record(line_number, WRONG_COLUMN_COUNT_CATEGORY, detail)  # Log it
            rejected_file.write(FIELD_SEPARATOR.join(fields) + "\n")  # Save for manual review
            rows_rejected += 1  # Count the rejection
            continue  # Skip to the next row
        cleaned_fields = clean_single_row(fields, line_number, issue_log)  # Trim and strip
        fingerprint = hash(tuple(cleaned_fields))  # Small stand-in for the whole row
        if fingerprint in seen_fingerprints:  # This exact row was already kept
            issue_log.record(line_number, DUPLICATE_CATEGORY)  # Log it
            continue  # Skip the duplicate
        seen_fingerprints.add(fingerprint)  # Remember this row
        fixed_file.write(FIELD_SEPARATOR.join(cleaned_fields) + "\n")  # Write the cleaned row
        rows_kept += 1  # Count the kept row
    del seen_fingerprints  # Release the memory used for duplicate detection
    return rows_read, rows_kept, rows_rejected  # Hand back the totals


# ----------------------------------------------------------------------
# Processing one file
# ----------------------------------------------------------------------
def fix_single_file(input_file_path):  # Runs the full workflow on one file
    fixed_file_path, rejected_file_path = build_output_file_paths(input_file_path)  # Output names
    encoding_name = detect_file_encoding(input_file_path)  # Find a working encoding
    width_counts = count_column_widths(input_file_path, encoding_name)  # First pass: widths
    expected_column_count = determine_expected_column_count(width_counts)  # Normal width
    issue_log = IssueLog(MAXIMUM_DETAIL_LINES_PER_FILE)  # Fresh log for this file
    with open(fixed_file_path, "w", encoding="utf-8", newline="\n") as fixed_file, \
            open(rejected_file_path, "w", encoding="utf-8", newline="\n") as rejected_file:  # Outputs
        rows_read, rows_kept, rows_rejected = stream_and_clean_rows(  # Second pass: clean
            input_file_path, encoding_name, expected_column_count,  # What to read
            fixed_file, rejected_file, issue_log,  # Where to write and log
        )  # End of cleaning
    if rows_rejected == 0:  # Nothing was rejected
        os.remove(rejected_file_path)  # Do not leave an empty rejects file behind
    file_summary = FileSummary(  # Bundle the results
        input_file_path, encoding_name, expected_column_count,  # Identification
        rows_read, rows_kept, rows_rejected, issue_log.total_issue_count,  # Numbers
    )  # End of summary
    return file_summary, issue_log  # Hand back both


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------
def generate_issue_summary_lines(issue_log):  # Yields one printable line per issue category
    for category, occurrence_count in issue_log.issue_counts.most_common():  # Most frequent first
        yield f"    {occurrence_count:>9,}  {category}"  # One formatted line


def print_file_report(file_summary, issue_log):  # Prints the report for one file
    display_path = os.path.relpath(file_summary.file_path, ROOT_DIRECTORY_PATH)  # Short path
    print(f"  encoding {file_summary.encoding_name} | columns {file_summary.expected_column_count}"
          f" | read {file_summary.rows_read:,} | kept {file_summary.rows_kept:,}"
          f" | rejected {file_summary.rows_rejected:,} | issues {file_summary.total_issue_count:,}")
    for summary_line in generate_issue_summary_lines(issue_log):  # Each category
        print(summary_line)  # Show it
    for detail_line in issue_log.detail_lines:  # The first few examples
        print(f"      e.g. {detail_line}")  # Show it
    assert display_path, "Display path must not be empty."  # Sanity check


def print_overall_summary(file_summaries, failed_files):  # Prints the closing summary
    total_read = sum(summary.rows_read for summary in file_summaries)  # All lines read
    total_kept = sum(summary.rows_kept for summary in file_summaries)  # All rows kept
    total_rejected = sum(summary.rows_rejected for summary in file_summaries)  # All rows rejected
    print("\n=== Overall ===")  # Section header
    print(f"Files processed: {len(file_summaries)} | failed: {len(failed_files)}")  # File counts
    print(f"Rows read {total_read:,} | kept {total_kept:,} | rejected {total_rejected:,}")  # Totals
    for failed_path, error_message in failed_files:  # Each failure
        print(f"FAILED {os.path.relpath(failed_path, ROOT_DIRECTORY_PATH)}: {error_message}")


# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------
def main():  # Runs the workflow over every .tsv file
    file_summaries = []  # Results for files that succeeded
    failed_files = []  # (path, message) for files that failed
    try:  # Guard the workflow so the closing message always prints
        input_file_paths = list(find_tsv_file_paths(ROOT_DIRECTORY_PATH))  # Collect every file
        print(f"Found {len(input_file_paths)} .tsv files under {ROOT_DIRECTORY_PATH}")  # Announce
        for input_file_path in input_file_paths:  # Handle each file in turn
            print(f"\n{os.path.relpath(input_file_path, ROOT_DIRECTORY_PATH)}")  # Show progress
            try:  # One bad file must not stop the others
                file_summary, issue_log = fix_single_file(input_file_path)  # Fix this file
            except (ValueError, OSError) as error:  # Empty, undecodable, or unreadable file
                failed_files.append((input_file_path, str(error)))  # Remember the failure
                print(f"  FAILED: {error}")  # Tell the person now
                continue  # Go on to the next file
            file_summaries.append(file_summary)  # Remember the success
            print_file_report(file_summary, issue_log)  # Show this file's report
        print_overall_summary(file_summaries, failed_files)  # Show the totals
    finally:  # Runs whether or not an error happened
        print("\nFinished. Originals were not modified.")  # Always signal completion


if __name__ == "__main__":  # Only run when executed directly, not when imported
    main()  # Start the program
