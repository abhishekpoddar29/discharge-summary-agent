import json
from pathlib import Path
from datetime import datetime

from crewai import Crew

from discharge_summary_agent.crew import DischargeSummaryAgentCrew
from discharge_summary_agent.tools.pdf_reader_tool import PDFReaderTool
from discharge_summary_agent.utils.document_chunker import chunk_text
from discharge_summary_agent.tools.medication_reconciliation_tool import (
    MedicationReconciliationTool,
)
from discharge_summary_agent.tools.conflict_detection_tool import (
    ConflictDetectionTool,
)
from discharge_summary_agent.tools.clinician_review_tool import (
    ClinicianReviewTool,
)

# =====================================================
# CONFIG
# =====================================================

PDF_PATH = "data/sample.pdf"

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 4000
CHUNK_OVERLAP = 500


# =====================================================
# STEP TRACE STRUCTURE
# =====================================================

step_trace = {
    "run_metadata": {
        "timestamp": str(datetime.now()),
        "pdf": PDF_PATH,
    },
    "pdf_extraction": {},
    "chunking": {},
    "chunk_extractions": [],
    "merged_evidence": {},
    "safety_review": {},
    "summary_generation": {}
}


# =====================================================
# HELPERS
# =====================================================

def safe_json(result):
    """Robust JSON parsing for CrewAI output"""
    if hasattr(result, "raw"):
        text = result.raw
    else:
        text = str(result)

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
    if text.startswith("```"):
        text = text.replace("```", "")
    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())


def safe_serialize(obj):
    """Ensure JSON serializable output"""
    return json.loads(json.dumps(obj, ensure_ascii=False))


def initialize_repository():
    return {
        "patient_demographics": [],
        "admission_date": [],
        "discharge_date": [],
        "principal_diagnosis": [],
        "secondary_diagnoses": [],
        "procedures": [],
        "allergies": [],
        "admission_medications": [],
        "discharge_medications": [],
        "hospital_course": [],
        "follow_up_instructions": [],
        "pending_results": [],
        "discharge_condition": [],
    }


def merge_evidence(master_repo, chunk_repo):
    for key in master_repo.keys():
        if key in chunk_repo and isinstance(chunk_repo[key], list):
            master_repo[key].extend(chunk_repo[key])
    return master_repo


# =====================================================
# STEP 1 : PDF EXTRACTION
# =====================================================

print("\n========== STEP 1 : PDF EXTRACTION ==========\n")

pdf_reader = PDFReaderTool()
pdf_result = pdf_reader.extract_text(PDF_PATH)

if not pdf_result["success"]:
    raise Exception(f"PDF extraction failed: {pdf_result.get('error')}")

full_text = pdf_result["text"]

step_trace["pdf_extraction"] = {
    "method": pdf_result.get("extraction_method"),
    "pages": pdf_result.get("pages"),
    "text_length": len(full_text),
    "status": "success"
}

print(f"Characters extracted: {len(full_text)}")


# =====================================================
# STEP 2 : CHUNKING
# =====================================================

print("\n========== STEP 2 : CHUNKING ==========\n")

chunks = chunk_text(
    text=full_text,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP,
)

step_trace["chunking"] = {
    "chunk_size": CHUNK_SIZE,
    "overlap": CHUNK_OVERLAP,
    "total_chunks": len(chunks)
}

print(f"Total chunks created: {len(chunks)}")


# =====================================================
# CREW INIT
# =====================================================

crew_instance = DischargeSummaryAgentCrew()

master_evidence = initialize_repository()


# =====================================================
# STEP 3 : EVIDENCE EXTRACTION LOOP
# =====================================================

print("\n========== STEP 3 : EVIDENCE EXTRACTION ==========\n")

for index, chunk in enumerate(chunks, start=1):

    print(f"\nProcessing Chunk {index}/{len(chunks)}")

    extraction_task = crew_instance.extract_patient_evidence()

    extraction_crew = Crew(
        agents=[crew_instance.document_analyst()],
        tasks=[extraction_task],
        verbose=True
    )

    result = extraction_crew.kickoff(
        inputs={
            "patient_documents": chunk,
            "chunk_number": index,
        }
    )

    chunk_trace = {
        "chunk_number": index,
        "input_length": len(chunk),
        "status": "success",
        "raw_output_preview": str(result)[:500]
    }

    try:
        chunk_json = safe_json(result)

        master_evidence = merge_evidence(master_evidence, chunk_json)

        chunk_trace["parsed"] = True

    except Exception as e:
        chunk_trace["parsed"] = False
        chunk_trace["error"] = str(e)

    step_trace["chunk_extractions"].append(chunk_trace)


# =====================================================
# SAVE MERGED EVIDENCE
# =====================================================

clean_master_evidence = safe_serialize(master_evidence)

step_trace["merged_evidence"] = {
    "total_fields_filled": sum(
        len(v) for v in master_evidence.values() if isinstance(v, list)
    )
}

merged_path = OUTPUT_DIR / "merged_evidence.json"

with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(clean_master_evidence, f, indent=2, ensure_ascii=False)

print(f"\nMerged evidence saved to {merged_path}")


# =====================================================
# STEP 4 : SAFETY REVIEW
# =====================================================

print("\n========== STEP 4 : SAFETY REVIEW ==========\n")

conflict_tool = ConflictDetectionTool()
med_tool = MedicationReconciliationTool()
review_tool = ClinicianReviewTool()


def ensure_dict(x):
    if isinstance(x, str):
        return json.loads(x)
    return x


conflict_results = ensure_dict(conflict_tool.run(master_evidence))
med_results = ensure_dict(
    med_tool.run(
        [i["value"] for i in master_evidence.get("admission_medications", [])],
        [i["value"] for i in master_evidence.get("discharge_medications", [])],
    )
)
review_results = ensure_dict(
    review_tool.run(
        evidence_repository=master_evidence,
        conflicts=conflict_results.get("conflicts", []),
    )
)

step_trace["safety_review"] = {
    "conflicts_found": len(conflict_results.get("conflicts", [])),
    "missing_fields": len(review_results.get("missing_fields", [])),
    "review_flags": len(review_results.get("review_flags", [])),
}

safety_report = {
    "missing_fields": review_results.get("missing_fields", []),
    "conflicts": conflict_results.get("conflicts", []),
    "medication_changes": med_results,
    "pending_results": master_evidence.get("pending_results", []),
    "review_flags": review_results.get("review_flags", []),
}

safety_path = OUTPUT_DIR / "safety_review.json"

with open(safety_path, "w", encoding="utf-8") as f:
    json.dump(safety_report, f, indent=2, ensure_ascii=False)

print(f"Safety report saved to {safety_path}")


# =====================================================
# STEP 5 : SUMMARY GENERATION
# =====================================================

print("\n========== STEP 5 : SUMMARY GENERATION ==========\n")

summary_task = crew_instance.generate_discharge_summary()

summary_crew = Crew(
    agents=[crew_instance.discharge_summary_generator()],
    tasks=[summary_task],
    verbose=True
)

summary_result = summary_crew.kickoff(
    inputs={
        "evidence_repository": master_evidence,
        "safety_review": safety_report,
    }
)

final_summary = (
    summary_result.raw
    if hasattr(summary_result, "raw")
    else str(summary_result)
)

step_trace["summary_generation"] = {
    "length": len(final_summary),
    "status": "generated"
}

summary_path = OUTPUT_DIR / "discharge_summary.md"

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(final_summary)

# =====================================================
# SAVE STEP TRACE (IMPORTANT FOR ASSIGNMENT)
# =====================================================

trace_path = OUTPUT_DIR / "step_trace.json"

with open(trace_path, "w", encoding="utf-8") as f:
    json.dump(step_trace, f, indent=2, ensure_ascii=False)

print(f"\nStep trace saved to {trace_path}")

print(f"\nDischarge summary saved to {summary_path}")

print("\n========== COMPLETED ==========\n")