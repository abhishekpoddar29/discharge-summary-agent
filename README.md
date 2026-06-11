# 🏥 Discharge Summary Agentic AI System

> **Turning messy hospital PDFs into crystal-clear, safety-aware clinical summaries — powered by a crew of specialized AI agents!** 🚀

[![CrewAI](https://img.shields.io/badge/Built%20with-CrewAI-blueviolet?style=for-the-badge)](https://crewai.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![UV](https://img.shields.io/badge/Package%20Manager-UV-orange?style=for-the-badge)](https://github.com/astral-sh/uv)

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

Three specialized agents. One shared mission: clinical accuracy.

### 🧠 1. Document Analyst Agent

The first responder. This agent digs through raw document text chunk by chunk and pulls out every clinical detail that matters:

- **Diagnoses** — primary, secondary, comorbidities
- **Medications** — names, doses, routes
- **Procedures** — what was done and when
- **Allergies** — substances and reaction types
- **Clinical events** — anything significant that happened during the stay

### ⚠️ 2. Clinical Safety Reviewer Agent

The quality gatekeeper. Once evidence is aggregated, this agent puts it all under a microscope and asks the hard questions:

- Are there **medication conflicts** between what was given and what was prescribed?
- Are **critical fields missing** that a clinician absolutely needs?
- Are there **clinical inconsistencies** that don't add up?

It wields three powerful tools to do this:
- 🔧 **Medication Reconciliation Tool** — compares admission vs. discharge meds
- 🔧 **Conflict Detection Tool** — surfaces contradictions across the document
- 🔧 **Clinician Review Tool** — flags uncertain or undocumented fields

### 📝 3. Discharge Summary Generator Agent

The final word. Takes all the validated, safety-reviewed evidence and converts it into a clean, structured discharge summary — ready for the clinician's desk.

- **Zero hallucinated facts** — only what was actually found in the document
- Any field that couldn't be confirmed is explicitly marked:

```
NOT DOCUMENTED — CLINICIAN REVIEW REQUIRED
```

Each agent hands off cleanly to the next, forming a pipeline where **accuracy compounds at every step**.

---

## 🔄 Workflow

```
📄 PDF Input
     │
     ▼
🔍 PDF Extraction (PyMuPDF + OCR)
     │
     ▼
✂️  Chunking Engine
     │
     ▼
🧠 CrewAI Document Analyst (per chunk)
     │
     ▼
🗂️  Evidence Aggregation
     │
     ▼
⚠️  Conflict Detection + 💊 Medication Reconciliation
     │
     ▼
🩺 Clinician Safety Review
     │
     ▼
📋 Final Discharge Summary Generation
     │
     ▼
📦 Outputs (JSON + Markdown + Step Trace)
```

---

## 📦 Project Structure

```
discharge_summary_agent/
│
├── src/
│   └── discharge_summary_agent/
│       ├── main.py                               # 🚀 Full pipeline orchestration
│       ├── crew.py                               # 🤖 CrewAI agents + tasks
│       ├── tools/
│       │   ├── pdf_reader_tool.py                # 🔍 PDF + OCR extraction
│       │   ├── conflict_detection_tool.py        # ⚠️  Contradiction finder
│       │   ├── medication_reconciliation_tool.py # 💊 Admission vs discharge med comparison
│       │   └── clinician_review_tool.py          # 🩺 Missing field & safety flag generator
│       ├── utils/
│       │   └── document_chunker.py               # ✂️  Smart document splitter
│       └── config/
│           ├── agents.yaml                       # ⚙️  Agent definitions
│           └── tasks.yaml                        # 📋 Task definitions
│
├── data/
│   └── sample.pdf                                # 📄 Sample discharge document
│
├── outputs/                                      # 📊 All generated results
│   ├── merged_evidence.json
│   ├── safety_review.json
│   ├── discharge_summary.md
│   └── step_trace.json
│
├── pyproject.toml                                # 📦 Project metadata & dependencies
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
 
Install all project dependencies in one shot:
 
```bash
uv pip install -e .
```
 
> 💡 This reads `pyproject.toml` and installs everything automatically.
 
Or install packages individually:
 
```bash
uv pip install "crewai[google-genai,tools]" \
               "google-generativeai>=0.8.6" \
               "pdfplumber>=0.11.9" \
               "pillow>=12.2.0" \
               "pymupdf>=1.26.7" \
               "pytesseract>=0.3.13" \
               "python-dotenv>=1.2.2"
```
 
Here's what each package brings to the party:
 
| Package | Purpose |
|---------|---------|
| `crewai[google-genai,tools]` | 🤖 Multi-agent framework + Google Gemini support + built-in tools |
| `google-generativeai` | 🧠 Google Gemini API client |
| `pdfplumber` | 📄 Precise text & table extraction from PDFs |
| `pillow` | 🖼️ Image processing for scanned document pages |
| `pymupdf` | ⚡ Fast PDF parsing and page rendering |
| `pytesseract` | 🔍 OCR engine wrapper for image-based PDFs |
| `python-dotenv` | 🔑 Loads API keys from your `.env` file |
 
> ⚠️ **Tesseract OCR** must also be installed at the system level for scanned PDF support:  
> **Mac:** `brew install tesseract`  
> **Ubuntu/Debian:** `sudo apt install tesseract-ocr`  
> **Windows:** Download the installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
 
> 🔑 **API Key Setup:** Create a `.env` file in the project root and add your Google Gemini API key:
> ```
> GEMINI_API_KEY=your_api_key_here
> ```

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

</div>
