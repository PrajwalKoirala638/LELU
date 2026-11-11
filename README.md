<div align="center">

# ⚖️🗽 LELU: Law Enforcement Lookup Data 🗽⚖️

### 🔍 Raw, machine-readable law enforcement misconduct data for New York City 🏙️

**📣 Data from [The Legal Aid Society of NYC](https://legalaidnyc.org)** · 🌐 [Live LELU app](https://legaidsoc.shinyapps.io/cap_search/) · ℹ️ [About LELU](https://legalaidnyc.org/law-enforcement-look-up/) · 🍴 [Upstream repo](https://github.com/the-legal-aid-society/LELU)

![Data: TSV + YAML](https://img.shields.io/badge/data-TSV%20%2B%20YAML-blue)
![Source: public records](https://img.shields.io/badge/source-public%20records-green)
![Folders: 9](https://img.shields.io/badge/data%20folders-9-purple)
![Fork](https://img.shields.io/badge/repo-fork%20of%20Legal%20Aid%20LELU-lightgrey)

</div>

---

> 🍴 **This is a fork.** The original, authoritative repository is [`the-legal-aid-society/LELU`](https://github.com/the-legal-aid-society/LELU), maintained by The Legal Aid Society. This fork adds documentation and example code. For the most current data, sync from or use the upstream repository.

---

## 📖 Table of Contents

1. [👀 At a glance](#-at-a-glance)
2. [❓ What is this?](#-what-is-this)
3. [🎁 Benefits](#-benefits)
4. [🗓️ Why it exists: the repeal of 50-a](#️-why-it-exists-the-repeal-of-50-a)
5. [🧭 About the data](#-about-the-data)
6. [🗂️ What's in each folder](#️-whats-in-each-folder)
7. [🚀 How to use this repo](#-how-to-use-this-repo)
8. [📊 Visualizing the data](#-visualizing-the-data)
9. [🧪 Validating and profiling](#-validating-and-profiling)
10. [📚 Data dictionary template](#-data-dictionary-template)
11. [🪪 Identifying officers responsibly](#-identifying-officers-responsibly)
12. [⚠️ Limitations and caveats](#️-limitations-and-caveats)
13. [🧑‍⚖️ Responsible use](#️-responsible-use)
14. [🔄 Keeping your copy up to date](#-keeping-your-copy-up-to-date)
15. [📝 Citing this data](#-citing-this-data)
16. [🤝 Support and contributions](#-support-and-contributions)
17. [📜 License and terms](#-license-and-terms)
18. [🔤 Glossary](#-glossary)
19. [🙋 FAQ](#-faq)
20. [🙏 Credits](#-credits)

---

## 👀 At a glance

|                         |                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| 🏛️ **Data from**        | The Legal Aid Society of NYC                                                                                 |
| 🎯 **Original purpose** | Support NYC LAS attorneys representing clients; shared with the public as a courtesy 🤲                      |
| 📁 **Format**           | One folder per LELU tab, each with `.tsv` data and `.yml` metadata                                           |
| 🗃️ **Folders**          | `ccrb`, `co`, `da_judicial`, `lawsuits`, `media`, `nypd_internal`, `payroll`, `payroll_historical`, `roster` |
| 🔄 **Updates**          | Upstream is updated each time LELU is updated                                                                |
| 🛠️ **Support level**    | Limited (see [Support](#-support-and-contributions))                                                         |

```mermaid
mindmap
  root((LELU data))
    🔎 Who uses it
      Attorneys
      Journalists
      Researchers
      Students
      Community members
    📦 What you get
      Raw TSV files
      YAML metadata
      9 data folders
    ⚠️ Handle with care
      Verify officer identity
      Read each source's About section
      Records are not findings
```

---

## ❓ What is this?

**Law Enforcement Lookup (LELU)** provides one-stop access to law enforcement misconduct data in New York City 🗽. It brings together many kinds of misconduct records that were historically hidden, so they can be searched in one place.

This repository holds the **raw data behind LELU** 📦. Each folder corresponds to one tab of the LELU app and contains:

| 📄 File type | 🎯 Purpose                                                                    |
| ------------ | ----------------------------------------------------------------------------- |
| `.tsv`       | The data itself, tab-separated, easy to load into Excel, R, Python, SQL, etc. |
| `.yml`       | Metadata describing the corresponding dataset                                 |

> 🎯 **Primary purpose of the original database:** to support NYC Legal Aid Society attorneys in representing their clients. It is shared with the public as a courtesy.

---

## 🎁 Benefits

| 🎁 Benefit                     | 💬 What it means for you                                                                       |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| 📦 **Many sources, one place** | Complaint, court, lawsuit, media, internal, payroll and roster data side by side               |
| 🧰 **Easy to use**             | Plain text files that open in Excel, Google Sheets, Python, R, SQL and DuckDB. No login or API |
| 🔓 **Transparency**            | Records that were secret until 50-a was repealed in 2020                                       |
| 🕰️ **Trackable history**       | Git history shows how the data changed between updates                                         |
| 🆓 **Free to access**          | No paywall and no special software                                                             |
| 🧪 **Great for projects**      | Research, journalism, courses, dashboards and civic-tech work                                  |
| 🏷️ **Documented**              | Each dataset ships with `.yml` metadata                                                        |

---

## 🗓️ Why it exists: the repeal of 50-a

For decades, New York's police secrecy law, **Civil Rights Law § 50-a** 🤐, kept law enforcement misconduct records shrouded in secrecy and withheld from the public. After **50-a was repealed on June 12, 2020** 🎉, state and city agencies began disclosing some misconduct records.

LELU exists to make those many forms of records accessible in one place 🧩, giving the public information needed to help achieve meaningful accountability ⚖️.

```mermaid
timeline
    title 🔓 From secrecy to disclosure
    Before June 2020 : 🤐 Police secrecy law 50-a keeps misconduct records confidential
    12 June 2020 : 🎉 50-a is repealed
    After repeal : 📂 State and city agencies begin disclosing some misconduct records
    Today : 🔍 LELU brings disclosed records together in one place
```

---

## 🧭 About the data

The data comes from **publicly disclosed records** about law enforcement in New York City, compiled and organized by The Legal Aid Society 🧑‍⚖️. A large share concerns the **NYPD** 👮, but different folders draw on different sources.

> 📌 **Provenance matters.** Each LELU tab has an **About** section on the [LELU site](https://legalaidnyc.org/law-enforcement-look-up/) describing where its data came from. Read it, along with the folder's `.yml` file, before relying on or republishing a dataset. The underlying records originate with the agencies that disclosed them.

```mermaid
flowchart LR
    A["🏢 Agencies disclose records<br/>after 50-a repeal"] --> B["🧑‍⚖️ Legal Aid Society<br/>collects and organizes"]
    B --> C["🌐 LELU web app<br/>one tab per source"]
    C --> D["📦 LELU repository<br/>TSV + YAML per tab"]
    D --> E["⚖️ Attorneys"]
    D --> F["📰 Researchers, journalists,<br/>and the public"]
```

---

## 🗂️ What's in each folder

Each folder matches a LELU tab. The descriptions below are based on the folder names; **always confirm in the folder's `.yml` files and the LELU About sections**.

| 📁 Folder            | 🧾 Likely contents (from the name)                            |
| -------------------- | ------------------------------------------------------------- |
| `ccrb`               | Records related to the Civilian Complaint Review Board        |
| `co`                 | See the folder's `.yml` and the LELU About section            |
| `da_judicial`        | Records connected to district attorneys and judicial findings |
| `lawsuits`           | Lawsuit-related records                                       |
| `media`              | Media-related records                                         |
| `nypd_internal`      | NYPD internal records                                         |
| `payroll`            | Payroll records                                               |
| `payroll_historical` | Historical payroll records                                    |
| `roster`             | Personnel roster records                                      |

```text
LELU/
├── 📄 README.md
├── 📁 ccrb/
├── 📁 co/
├── 📁 da_judicial/
├── 📁 lawsuits/
├── 📁 media/
├── 📁 nypd_internal/
├── 📁 payroll/
├── 📁 payroll_historical/
└── 📁 roster/
    └── each folder: 📊 *.tsv  +  🏷️ *.yml
```

```mermaid
flowchart TD
    R["📦 LELU"] --> A["📁 ccrb"]
    R --> B["📁 co"]
    R --> C["📁 da_judicial"]
    R --> D["📁 lawsuits"]
    R --> E["📁 media"]
    R --> F["📁 nypd_internal"]
    R --> G["📁 payroll"]
    R --> H["📁 payroll_historical"]
    R --> I["📁 roster"]
```

---

## 🚀 How to use this repo

### 👀 1. Browse on GitHub

Open a folder, then click a `.tsv` file to preview the rows. Click a `.yml` file to read its metadata.

### 📥 2. Download

**No Git:** click the green **Code** button → **Download ZIP**.

**With Git:**

```bash
git clone https://github.com/PrajwalKoirala638/LELU.git
cd LELU
```

### 📊 3. Open in a spreadsheet

In Excel or Google Sheets, import the file as **tab-delimited** (Data → From Text/CSV, or File → Import).

### 🐍 4. Python (pandas)

```python
import pandas as pd

df = pd.read_csv("ccrb/<dataset>.tsv", sep="\t", dtype=str)
print(df.shape)
print(df.columns.tolist())
print(df.head())
```

### 📈 5. R

```r
library(readr)

df <- read_tsv("ccrb/<dataset>.tsv", col_types = cols(.default = "c"))
glimpse(df)
```

### 💻 6. Command line

```bash
# list every data file
find . -name "*.tsv"

# row count (minus header)
tail -n +2 ccrb/<dataset>.tsv | wc -l

# preview the columns
head -n 1 ccrb/<dataset>.tsv | tr '\t' '\n'
```

### 🦆 7. DuckDB (SQL on the raw files)

```sql
SELECT *
FROM read_csv_auto('ccrb/<dataset>.tsv', delim='\t', all_varchar=true)
LIMIT 10;
```

### 🏷️ 8. Read the metadata

```python
import yaml

with open("ccrb/<dataset>.yml") as f:
    print(yaml.safe_load(f))
```

> 💡 **Tip:** read identifier-like columns (IDs, tax IDs, shield numbers) **as text** so leading zeros are not dropped.

```mermaid
flowchart LR
    A["👀 Browse"] --> B["📥 Download or clone"]
    B --> C["🏷️ Read the .yml"]
    C --> D["📊 Load the .tsv"]
    D --> E["🔬 Analyze and chart"]
    E --> F["✅ Verify before publishing"]
```

---

## 📊 Visualizing the data

📉 Counts change with every update, so this repo does not ship fixed statistics. These recipes generate charts from the current files, so the numbers are always accurate ✅. Replace the `<...>` placeholders with real names from the dataset you're using.

### 📅 Records per year

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("<folder>/<dataset>.tsv", sep="\t", dtype=str)

df["year"] = pd.to_datetime(df["<date-column>"], errors="coerce").dt.year
counts = df["year"].value_counts().sort_index()

counts.plot(kind="bar", figsize=(10, 4), title="Records per year")
plt.xlabel("Year")
plt.ylabel("Records")
plt.tight_layout()
plt.savefig("records_per_year.png", dpi=150)
```

### 🏷️ Top categories

```python
top = df["<category-column>"].value_counts().head(15)
top.sort_values().plot(kind="barh", figsize=(8, 6), title="Most common categories")
plt.tight_layout()
plt.savefig("top_categories.png", dpi=150)
```

### 🗺️ By precinct (R)

```r
library(dplyr); library(ggplot2); library(readr)

df <- read_tsv("<folder>/<dataset>.tsv", col_types = cols(.default = "c"))

df |>
  count(`<precinct-column>`, sort = TRUE) |>
  slice_head(n = 20) |>
  ggplot(aes(reorder(`<precinct-column>`, n), n)) +
  geom_col() +
  coord_flip() +
  labs(x = NULL, y = "Records", title = "Records by precinct (top 20)")
```

### 🔥 Month-by-year heatmap

```python
import seaborn as sns

d = pd.to_datetime(df["<date-column>"], errors="coerce").dropna()
pivot = (
    pd.DataFrame({"year": d.dt.year, "month": d.dt.month})
    .value_counts().unstack(fill_value=0).sort_index()
)
sns.heatmap(pivot, cmap="YlOrRd")
plt.title("Records by year and month")
plt.savefig("heatmap.png", dpi=150)
```

### 🧩 Missing-data chart

```python
missing = df.isna().mean().sort_values(ascending=False).head(20) * 100
missing.plot(kind="barh", figsize=(8, 6), title="% missing by column")
plt.tight_layout()
plt.savefig("missing.png", dpi=150)
```

### 💡 Ideas

- 📈 Trends over time
- 🗺️ Geographic breakdowns
- 🏷️ Category or outcome comparisons
- 🕳️ Where data is missing, and what that says about disclosure
- 🔗 Cross-folder comparison (see the caution on identifiers below)

---

## 🧪 Validating and profiling

### 📋 Profile every folder at once

```python
from pathlib import Path
import pandas as pd

rows = []
for f in Path(".").rglob("*.tsv"):
    df = pd.read_csv(f, sep="\t", dtype=str)
    rows.append({"folder": f.parts[0], "file": f.name,
                 "rows": len(df), "columns": df.shape[1]})

summary = pd.DataFrame(rows).sort_values(["folder", "file"])
print(summary.to_markdown(index=False))
```

Paste the output below to keep a dated snapshot 📸:

| 📁 Folder   | 📄 File     | 🔢 Rows | 🧱 Columns | 📅 Snapshot date |
| ----------- | ----------- | ------: | ---------: | ---------------- |
| _generated_ | _generated_ |     _n_ |        _n_ | _YYYY-MM-DD_     |

### ✅ Sanity checks after each update

```python
from pathlib import Path
import pandas as pd

for f in Path(".").rglob("*.tsv"):
    df = pd.read_csv(f, sep="\t", dtype=str)
    assert df.shape[1] > 1, f"{f}: only one column, check the delimiter"
    print(f"{f}: {len(df)} rows, {df.duplicated().sum()} exact duplicate rows")
```

### 🤖 Optional: GitHub Actions summary

Save the profiling script as `scripts/profile.py`, then add `.github/workflows/profile.yml`:

```yaml
name: Profile data
on:
  push:
    paths: ["**/*.tsv"]
jobs:
  profile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pandas tabulate
      - run: python scripts/profile.py >> $GITHUB_STEP_SUMMARY
```

---

## 📚 Data dictionary template

Copy this for each dataset 📝 and fill it in from the `.yml` file and the LELU About section.

| 🏷️ Column  | 🧾 Description  | 🔤 Type              | ❓ Can be blank? | 📝 Notes  |
| ---------- | --------------- | -------------------- | ---------------- | --------- |
| `<column>` | _what it means_ | text / date / number | yes / no         | _caveats_ |

**Per-dataset checklist** ✔️

- [ ] 🌐 Source agency and how the records were obtained
- [ ] 📅 Date range covered
- [ ] 🔄 Date of last refresh
- [ ] 🪪 Which officer identifiers are present (Tax ID, shield, name)
- [ ] ⚠️ Known gaps or quirks

---

## 🪪 Identifying officers responsibly

🧑‍⚖️ LELU users are responsible for determining whether the results returned represent the officer in question.

The misconduct sources vary in how much they identify each individual officer. For NYPD officers, **the only stable and unique identifier is the "Tax ID"** 🔑, and it is **not consistently available** from every source. These are **not** reliable identifiers:

| 🏷️ Field                 | 🎯 Reliable?   | 💬 Why                                 |
| ------------------------ | -------------- | -------------------------------------- |
| 🔑 Tax ID                | ✅ Most stable | Not present in all sources             |
| 🛡️ Shield / badge number | ⚠️ No          | Can change or be reassigned            |
| 🏢 Precinct / command    | ⚠️ No          | Officers transfer                      |
| 👤 Name                  | ⚠️ No          | Changes, duplicates, spelling variants |

This is why **LELU does not build a single "profile" page per officer** 🚫👤. Please do not merge records across folders by name or badge alone, and treat any match as a lead to verify, not a conclusion.

```mermaid
flowchart TD
    A["🔍 Found a matching record"] --> B{"🔑 Same Tax ID<br/>in both sources?"}
    B -- "✅ Yes" --> C["💪 Strongest match,<br/>still verify"]
    B -- "❌ No or unavailable" --> D["🛑 Do not assume<br/>same person"]
    D --> E["🕵️ Verify with additional evidence<br/>before drawing any conclusion"]
```

---

## ⚠️ Limitations and caveats

- 🧾 **Records are not findings.** A record's presence does not by itself establish what happened.
- 🧩 **Coverage is uneven.** Agencies disclosed records at different times and in different formats.
- 🚫 **No unified officer identity.** See the identifier section above.
- 🕳️ **Data reflects disclosure, not reality.** Missing records may simply mean nothing was disclosed.
- 🛑 **No adverse decisions about an individual** without independent verification.
- ⏳ **Forks and snapshots age.** Check the upstream repo and the LELU page for the latest data.

---

## 🧑‍⚖️ Responsible use

```mermaid
flowchart LR
    A["📥 Download data"] --> B["📖 Read the source's<br/>About section"]
    B --> C["🧹 Clean and analyze"]
    C --> D["✅ Verify any individual match"]
    D --> E["📣 Publish with context<br/>and a data date"]
```

- 🤝 Present findings with context, not as standalone accusations
- 🔬 Be transparent about methods and limitations
- 🧍 Remember that real people appear in these records, including civilians

---

## 🔄 Keeping your copy up to date

This fork does not update itself. To pull the latest data from Legal Aid's repository:

```bash
git remote add upstream https://github.com/the-legal-aid-society/LELU.git
git fetch upstream
git merge upstream/main
```

Or use the **Sync fork** button on the GitHub page of your fork 🔄. The LELU site shows its own "last updated" date 📅.

---

## 📝 Citing this data

> The Legal Aid Society of NYC. _Law Enforcement Lookup (LELU)_. https://legalaidnyc.org/law-enforcement-look-up/. Accessed YYYY-MM-DD.

```bibtex
@misc{lelu,
  author       = {{The Legal Aid Society of NYC}},
  title        = {Law Enforcement Lookup (LELU)},
  howpublished = {\url{https://legalaidnyc.org/law-enforcement-look-up/}},
  note         = {Accessed: YYYY-MM-DD}
}
```

---

## 🤝 Support and contributions

🏗️ The Legal Aid Society does not have the organizational capacity to support full-stack application development, so it is limited in its ability to provide documentation or updates, make improvements, or collaborate with outside parties.

- 📚 For questions about the **data**, see the LELU site and the upstream repository.
- 🛠️ For questions about this fork's **documentation and example code**, open an issue here.
- 🙏 Please understand that issues and pull requests may not receive a response.

---

## 📜 License and Terms

⚖️ **MIT License**

This project is released under the **MIT License**, one of the most permissive open-source licenses.

- 📂 **Data:** The data was originally compiled and published by The Legal Aid Society of NYC. The MIT License applies only to original materials owned by this project's author. It does not automatically grant rights to third-party data. Please review the Legal Aid Society's [Terms of Use](https://legalaidnyc.org/terms-of-use/) and [Disclaimer](https://legalaidnyc.org/disclaimer/) before redistributing, modifying, or using the data commercially.

- 🧑‍💻 **Original code and documentation:** All original code, scripts, chart configurations, documentation, and README content created for this repository are licensed under the MIT License.

- 🚫 **Third-party content:** Data, materials, trademarks, and other content owned by third parties remain subject to their respective licenses, terms, and restrictions. The repository author does not claim ownership of or grant additional rights to such materials.

- 🤝 **Contributions:** Contributions to original project materials are subject to the MIT License unless otherwise specified.

See the [LICENSE](LICENSE) file for the complete license text.

---

## 🔤 Glossary

| 🔤 Term           | 💬 Meaning                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **LELU**          | Law Enforcement Lookup, Legal Aid's tool for law enforcement misconduct data in NYC        |
| **50-a**          | New York Civil Rights Law § 50-a, the police secrecy law repealed on June 12, 2020         |
| **Tax ID**        | The only stable, unique identifier for NYPD officers, though not available in every source |
| **TSV**           | Tab-separated values, a plain-text table format                                            |
| **YAML (`.yml`)** | A human-readable format used here for dataset metadata                                     |
| **Fork**          | A personal copy of a GitHub repository                                                     |
| **LAS**           | The Legal Aid Society                                                                      |

---

## 🙋 FAQ

**🧐 Is this all NYPD data?**
Much of it concerns the NYPD 👮, but sources vary by folder. Check each folder's `.yml` and the LELU About sections.

**🔎 Can I search officers by name here?**
Use the [LELU app](https://legaidsoc.shinyapps.io/cap_search/) 🌐 for searching. This repository is for raw files.

**🗂️ Why TSV instead of CSV?**
Tabs rarely appear inside text fields, which makes parsing more robust than commas.

**⏱️ How do I know the data is current?**
Compare this fork's commits with the upstream repo, and check the "last updated" date on the LELU page 🕰️.

**🔗 Can I link records across folders?**
Only with great care. See the identifier section.

**🆘 I need legal help. Can you help?**
This repo can't give legal advice. Legal Aid's help line is **212-577-3300** 📞.

---

## 🙏 Credits

💙 Data compiled and published by **The Legal Aid Society**, New York City.

- 🌐 Website: <https://legalaidnyc.org>
- 🔍 LELU: <https://legalaidnyc.org/law-enforcement-look-up/>
- 🍴 Upstream repo: <https://github.com/the-legal-aid-society/LELU>
- 📞 Free legal help: call **212-577-3300**

<div align="center">

⚖️ _Transparency is critical to accountability._ ⚖️

</div>
