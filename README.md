🏥 Discharge Summary Agent — AI Clinical Documentation System

Welcome to the Discharge Summary Agent — an intelligent multi-agent system that reads messy hospital PDFs, extracts structured clinical evidence, detects inconsistencies, and generates a clinician-ready discharge summary draft.

Built using CrewAI + LLM agents + medical safety tools, this project simulates a real-world hospital documentation pipeline powered by AI.

🌟 What this project does

Given a raw hospital discharge PDF, the system:

📄 Extracts text (OCR + PDF parsing)
✂️ Splits into intelligent chunks
🧠 Runs a Clinical Document Analyst agent per chunk
📦 Merges structured medical evidence
⚠️ Runs safety + medication + conflict analysis
📝 Generates a final discharge summary draft

Everything is fully automated and traceable step-by-step.

🤖 Crew Architecture (Agents)

This project is powered by 3 intelligent agents:

🧠 1. Document Analyst Agent
Extracts structured medical data from raw text
Identifies:
Diagnoses
Medications
Procedures
Allergies
Clinical events
⚠️ 2. Clinical Safety Reviewer Agent
Detects:
Medication conflicts
Missing critical fields
Clinical inconsistencies
Uses tools:
Medication Reconciliation Tool
Conflict Detection Tool
Clinician Review Tool
📝 3. Discharge Summary Generator Agent
Converts validated evidence into a clean discharge summary
Ensures:
No hallucinated facts

Missing data marked as:

NOT DOCUMENTED - CLINICIAN REVIEW REQUIRED
🔁 Workflow Diagram
PDF Input
   ↓
Text Extraction (PyMuPDF / OCR)
   ↓
Chunking (Overlapping windows)
   ↓
Document Analyst Agent (per chunk)
   ↓
Merged Structured Evidence
   ↓
Safety & Conflict Review
   ↓
Discharge Summary Generator
   ↓
Final Report + Step Trace Output
📁 Project Structure
discharge_summary_agent/
│
├── src/discharge_summary_agent/
│   ├── main.py                  # Full pipeline orchestration
│   ├── crew.py                 # CrewAI agents + tasks
│   ├── tools/
│   │   ├── pdf_reader_tool.py
│   │   ├── conflict_detection_tool.py
│   │   ├── medication_reconciliation_tool.py
│   │   └── clinician_review_tool.py
│   │
│   ├── utils/
│   │   └── document_chunker.py
│   │
│   └── config/
│       ├── agents.yaml
│       └── tasks.yaml
│
├── data/
│   └── sample.pdf
│
├── outputs/
│   ├── merged_evidence.json
│   ├── safety_review.json
│   ├── discharge_summary.md
│   └── step_trace.json
│
├── README.md
└── pyproject.toml
⚙️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/discharge-summary-agent.git
cd discharge-summary-agent
2️⃣ Create UV Virtual Environment
uv venv

Activate it:

Windows:
.venv\Scripts\activate
Mac/Linux:
source .venv/bin/activate
3️⃣ Install Dependencies
uv pip install -r requirements.txt

Or if using pyproject:

uv pip install crewai pymupdf pytesseract pillow
4️⃣ Install System Dependencies
Tesseract OCR required:
Windows: Install from https://github.com/tesseract-ocr/tesseract
Linux:
sudo apt install tesseract-ocr
🚀 Run the Project
python src/discharge_summary_agent/main.py