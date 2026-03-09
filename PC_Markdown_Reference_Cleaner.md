# PMC Markdown Reference Cleaner

A small **Python + PyQt6 GUI tool** to automatically clean references copied from **PubMed Central (PMC)**.

When references are copied from the PMC website:

https://pmc.ncbi.nlm.nih.gov/

the generated Markdown often contains problems such as:

* escaped brackets `\[ \]`
* unnecessary links like `[PMC free article]`
* spaces between reference links
* empty brackets `[]`

This program automatically cleans the text so it is ready to use in **Markdown**, **blogs**, **technical documentation**, or **scientific articles**.

---

# Features

The program automatically fixes:

* `\[text\]` → `[text]`
* removes `[PMC free article]` links
* merges reference links like:

```text
[DOI](...)[PubMed](...)[Google Scholar](...)
```

* removes empty brackets `[]`
* allows you to:

✔ paste text
✔ fix Markdown
✔ copy the result
✔ save as `.md`

---

# Example

### Input

```text
- 2.Hou K., Wu Z.-X., Chen X.-Y., Wang J.-Q., Zhang D., Xiao C., Zhu D., Koya J.B., Wei L., Li J., et al. Microbiota in health and diseases. Signal Transduct. Target. Ther. 2022;7:135. doi: 10.1038/s41392-022-00974-4. \[[DOI](https://doi.org/10.1038/s41392-022-00974-4)\] \[[PMC free article](/articles/PMC9034083/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)\] \[[Google Scholar](https://scholar.google.com/...)\]
```

### Output

```text
- 2.Hou K., Wu Z.-X., Chen X.-Y., Wang J.-Q., Zhang D., Xiao C., Zhu D., Koya J.B., Wei L., Li J., et al. Microbiota in health and diseases. Signal Transduct. Target. Ther. 2022;7:135. doi: 10.1038/s41392-022-00974-4. [DOI](https://doi.org/10.1038/s41392-022-00974-4)[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)[Google Scholar](https://scholar.google.com/...)
```

---

# Requirements

* Python **3.9 or newer**
* PyQt6

---

# Installation

## Windows

1. Install Python

Download from:

https://www.python.org/downloads/

During installation **enable the option**:

```
Add Python to PATH
```

2. Install PyQt6

Open **Command Prompt** or **PowerShell**:

```
pip install PyQt6
```

3. Run the program

```
python arreglar_referencias_pmc.py
```

---

## Linux

Most Linux distributions already include Python.

Check:

```
python3 --version
```

Install PyQt6:

```
pip install PyQt6
```

Run the program:

```
python3 arreglar_referencias_pmc.py
```

---

## macOS

1. Check Python:

```
python3 --version
```

If Python is not installed:

```
brew install python
```

2. Install PyQt6

```
pip3 install PyQt6
```

3. Run the program

```
python3 arreglar_referencias_pmc.py
```

---

# Usage

1. Copy references from **PubMed Central**
2. Paste them into the left panel
3. Click:

```
Fix Markdown
```

Optional:

```
Remove empty []
```

4. Copy or save the cleaned result.

---

# Recommended Workflow

1️⃣ Open an article at:

https://pmc.ncbi.nlm.nih.gov/

2️⃣ Go to **References**

3️⃣ Use a browser extension such as:

**Selection Copilot**

https://microsoftedge.microsoft.com/addons/detail/copiloto-de-selección/ignppgbmdpkamckbgakeofhlbnonpopn

4️⃣ Copy the references in Markdown.

5️⃣ Paste them into the program and clean them.

---

# License

MIT License

---

# Author

Tool created to clean Markdown references copied from **PubMed Central (PMC)**.
