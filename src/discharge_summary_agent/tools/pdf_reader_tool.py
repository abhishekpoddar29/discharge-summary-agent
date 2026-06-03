from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


class PDFReaderTool:
    """
    Extract text from PDFs.

    Strategy:
    1. Try direct text extraction.
    2. If extracted text is empty, use OCR.
    3. Never crash the workflow.
    """

    def extract_text(self, pdf_path: str) -> dict:
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            return {
                "success": False,
                "error": f"File not found: {pdf_path}"
            }

        try:
            doc = fitz.open(pdf_path)

            extracted_text = []
            page_count = len(doc)

            # ---------- Attempt Direct Text Extraction ----------
            for page in doc:
                text = page.get_text("text")
                if text.strip():
                    extracted_text.append(text)

            full_text = "\n".join(extracted_text).strip()

            # ---------- If Text Found ----------
            if len(full_text) > 100:
                return {
                    "success": True,
                    "filename": pdf_file.name,
                    "pages": page_count,
                    "extraction_method": "text",
                    "text": full_text
                }

            # ---------- OCR Fallback ----------
            ocr_text = []

            for page_num in range(page_count):
                page = doc.load_page(page_num)

                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                image_bytes = pix.tobytes("png")

                image = Image.open(io.BytesIO(image_bytes))

                page_text = pytesseract.image_to_string(image)

                ocr_text.append(page_text)

            full_ocr_text = "\n".join(ocr_text).strip()

            return {
                "success": True,
                "filename": pdf_file.name,
                "pages": page_count,
                "extraction_method": "ocr",
                "text": full_ocr_text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }