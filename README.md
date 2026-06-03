# 🏥 Discharge Summary Agentic AI System

> **Turning messy hospital PDFs into crystal-clear, safety-aware clinical summaries — powered by a crew of specialized AI agents!** 🚀

[![CrewAI](https://img.shields.io/badge/Built%20with-CrewAI-blueviolet?style=for-the-badge)](https://crewai.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![UV](https://img.shields.io/badge/Package%20Manager-UV-orange?style=for-the-badge)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🌟 What Is This?

The **Discharge Summary Agent** is a fully agentic, multi-agent AI pipeline that reads real-world hospital discharge documents — the noisy, inconsistent, sometimes-scanned-sideways kind — and transforms them into **structured, clinically safe summaries** that actually make sense.

No hallucinations. No guessing. No shortcuts.  
Just a disciplined crew of AI agents doing what they do best. 🧠⚕️

---

## ✨ Features

### 🧾 PDF Intelligence
- Extracts text from both **digital and scanned PDFs**
- OCR fallback via **Tesseract** for low-quality or image-based documents
- Handles the real world — rotations, noise, messy formatting, all of it

### 🧠 Multi-Agent Extraction Engine
- Splits documents into **manageable chunks** for precision
- Each chunk is independently analyzed by a **CrewAI Document Analyst agent**
- Extracts key clinical entities:
  - 🩺 Diagnoses
  - 💊 Medications
  - 🔬 Procedures
  - ⚠️ Allergies
  - 📅 Admission & Discharge details

### 🛡️ Clinical Safety Engine
- Detects **conflicting medical information** across document sections
- **Never guesses** missing data — unknown is unknown
- Escalates uncertainty with explicit clinician review flags

### 💊 Medication Reconciliation
- Compares **admission vs. discharge** medication lists
- Automatically surfaces any changes, additions, or removals

### 🧑‍⚕️ Final Discharge Summary Generator
- Produces a **structured, clinician-ready** summary
- Missing fields are never silently skipped — they're clearly marked:
  > `NOT DOCUMENTED — CLINICIAN REVIEW REQUIRED`

### 📊 Full Step Trace Logging
- Every stage logged end-to-end:
  - PDF extraction → chunking → evidence merging → safety review → summary generation
- Perfect for **audits, evaluations, and debugging**

---

## 🤖 Meet the Crew

Five specialized agents. One shared mission: clinical accuracy.

| # | Agent | Role |
|---|-------|------|
| 1️⃣ | **Senior Clinical Document Analyst** | Extracts structured medical entities from each document chunk |
| 2️⃣ | **Conflict Detection Agent** | Hunts down contradictions in diagnoses, dates, procedures, and allergies |
| 3️⃣ | **Medication Reconciliation Agent** | Compares admission and discharge medication lists, flags every change |
| 4️⃣ | **Clinician Review Agent** | Flags uncertain or missing fields and generates review warnings |
| 5️⃣ | **Discharge Summary Generator** | Converts all validated evidence into the final structured report |

Each agent is purpose-built, working in sequence to ensure **no detail slips through the cracks**.

---

## 🔄 Workflow

```
📄 PDF Input
     │
     ▼
🔍 PDF Extraction (PyMuPDF + OCR Fallback)
     │
     ▼
✂️  Chunking Engine
     │
     ▼
🧠 CrewAI Document Analyst  ◄── (runs per chunk)
     │
     ▼
🗂️  Evidence Aggregation
     │
     ├──► ⚠️  Conflict Detection
     │
     ├──► 💊 Medication Reconciliation
     │
     ▼
🩺 Clinician Safety Review
     │
     ▼
📋 Final Discharge Summary Generation
     │
     ▼
📦 Outputs: JSON + Markdown + Step Trace
```

---

## 📦 Project Structure

```
discharge_summary_agent/
│
├── src/
│   └── discharge_summary_agent/
│       ├── main.py                          # 🚀 Entry point
│       ├── crew.py                          # 🤖 CrewAI crew definition
│       ├── config/                          # ⚙️  Agent & task configs
│       ├── tools/
│       │   ├── pdf_reader_tool.py           # 🔍 PDF + OCR extraction
│       │   ├── conflict_detection_tool.py   # ⚠️  Contradiction finder
│       │   ├── medication_reconciliation_tool.py  # 💊 Med comparison
│       │   └── clinician_review_tool.py     # 🩺 Safety flag generator
│       ├── utils/
│       │   └── document_chunker.py          # ✂️  Smart document splitter
│       └── agents/                          # 🧠 Agent definitions
│
├── data/
│   ├── sample.pdf                           # 📄 Test patient 1
│   └── sample_patient_2.pdf                 # 📄 Test patient 2
│
├── outputs/                                 # 📊 All generated results
│   ├── merged_evidence.json
│   ├── safety_review.json
│   ├── discharge_summary.md
│   └── step_trace.json
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/discharge-summary-agent.git
cd discharge-summary-agent
```

### 2️⃣ Create a Virtual Environment with UV

> 💡 **UV** is a blazing-fast Python package manager. If you don't have it, install it first:  
> `pip install uv`

```bash
uv venv
```

Activate your environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
uv pip install -r requirements.txt
```

> ⚠️ Tesseract OCR must also be installed on your system for scanned PDF support.  
> Mac: `brew install tesseract` | Ubuntu: `sudo apt install tesseract-ocr`

### 4️⃣ Add Your PDF

Drop your hospital discharge PDF into the `data/` folder, or use the included samples.

### 5️⃣ Run the Pipeline 🎉

```bash
uv run python src/discharge_summary_agent/main.py
```

Sit back and watch the crew get to work!

---

## 📤 Outputs

After a successful run, four files are generated inside the `outputs/` folder:

### 📄 `merged_evidence.json`
All extracted clinical entities from across every document chunk, aggregated into one structured JSON object.

### ⚠️ `safety_review.json`
A full conflict detection and clinician review report — every inconsistency flagged, every missing field identified, every concern escalated.

### 🧾 `discharge_summary.md`
The crown jewel. A clean, structured, clinician-ready discharge summary in Markdown format. Fields that couldn't be confirmed are explicitly marked:
```
NOT DOCUMENTED — CLINICIAN REVIEW REQUIRED
```

### 🔬 `step_trace.json`
A complete trace of every pipeline step — which agents ran, what they processed, and what decisions were made. Invaluable for evaluation, auditing, and debugging.

---

## 🧪 Example Output Snippet

```markdown
## 🏥 Discharge Summary

**Patient Name:** John Doe  
**Admission Date:** 2024-03-01  
**Discharge Date:** 2024-03-07  

### Primary Diagnosis
Acute Myocardial Infarction (STEMI)

### Discharge Medications
| Medication      | Dose   | Change    |
|----------------|--------|-----------|
| Aspirin         | 75mg   | Continued |
| Atorvastatin    | 40mg   | New       |
| Metoprolol      | 25mg   | New       |

### Allergies
Penicillin — Anaphylaxis

### Follow-up
⚠️ NOT DOCUMENTED — CLINICIAN REVIEW REQUIRED
```

---

## 🛡️ Clinical Safety Philosophy

This system is designed with **patient safety as the #1 priority**:

- **No hallucination policy** — if data isn't in the document, it won't appear in the output
- **Conflict escalation** — contradictions between document sections are surfaced, never silently resolved
- **Explicit uncertainty** — every unknown is labeled, never assumed
- **Full audit trail** — every decision traceable via step trace

---

## 🤝 Contributing

Got ideas to make this even safer or smarter? PRs are welcome!  
Please open an issue first to discuss major changes.

---


Built with ❤️ using [CrewAI](https://crewai.com) · Powered by multi-agent reasoning · Designed for clinical safety

</div>
