from __future__ import annotations

from pathlib import Path


def extract_docx_text(file_path: Path) -> str:
    # Lazy import to keep module import cheap.
    from docx import Document

    doc = Document(str(file_path))
    paragraphs = [p.text for p in doc.paragraphs if p.text is not None]
    return "\n".join([p for p in paragraphs if p.strip() != ""]).strip()
