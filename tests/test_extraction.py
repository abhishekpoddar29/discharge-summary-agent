import json

from crewai import Crew

from discharge_summary_agent.crew import DischargeSummaryAgentCrew
from discharge_summary_agent.tools.pdf_reader_tool import PDFReaderTool
from discharge_summary_agent.utils.document_chunker import chunk_text


PDF_PATH = "data/sample.pdf"


def main():

    print("\n========== PDF EXTRACTION ==========\n")

    pdf_reader = PDFReaderTool()

    pdf_result = pdf_reader.extract_text(PDF_PATH)

    if not pdf_result["success"]:
        print("PDF extraction failed")
        print(pdf_result)
        return

    full_text = pdf_result["text"]

    print(f"Text Length: {len(full_text)}")

    print("\n========== CHUNKING ==========\n")

    chunks  = chunk_text(
        text=full_text,
        chunk_size=4000,
        overlap=500
    )

    print(f"Total Chunks: {len(chunks)}")

    if not chunks:
        print("No chunks generated")
        return

    first_chunk = chunks[0]
    

    print(
        f"First Chunk Length: {len(first_chunk)}"
    )
    print(first_chunk[:3000])

    print("\n========== CREW INITIALIZATION ==========\n")

    crew_instance = DischargeSummaryAgentCrew()

    extraction_task = (
        crew_instance.extract_patient_evidence()
    )

    extraction_crew = Crew(
        agents=[
            crew_instance.document_analyst()
        ],
        tasks=[
            extraction_task
        ],
        verbose=True
    )

    print(
        "\n========== RUNNING DOCUMENT ANALYST ==========\n"
    )

    result = extraction_crew.kickoff(
        inputs={
            "patient_documents": first_chunk,
            "chunk_number": 1,
            "total_chunks": len(chunks),
        }
    )

    print(
        "\n========== RAW RESULT ==========\n"
    )

    if hasattr(result, "raw"):
        print(result.raw)

        try:
            cleaned_output = result.raw.strip()

            if cleaned_output.startswith("```json"):
                cleaned_output = cleaned_output.replace("```json", "", 1)

            if cleaned_output.endswith("```"):
                cleaned_output = cleaned_output[:-3]

            cleaned_output = cleaned_output.strip()

            parsed = json.loads(cleaned_output)

            print(
                "\n========== JSON VALIDATION SUCCESS ==========\n"
            )

            print(
                json.dumps(
                    parsed,
                    indent=2
                )
            )

        except Exception as e:

            print(
                "\n========== JSON VALIDATION FAILED ==========\n"
            )

            print(e)

    else:

        print(result)


if __name__ == "__main__":
    main()