from __future__ import annotations

from pathlib import Path


def extract_pdf_text(file_path: Path) -> tuple[str, int | None]:
    # PyMuPDF
    import fitz  # type: ignore

    doc = fitz.open(str(file_path))
    try:
        texts: list[str] = []
        for page in doc:
            texts.append(page.get_text("text"))
        text = "\n".join(t.strip("\n") for t in texts).strip()
        return text, doc.page_count
    finally:
        doc.close()
