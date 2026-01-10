from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path

from app.services.converters.docx_converter import extract_docx_text
from app.services.converters.hwp_converter import extract_hwp_text
from app.services.converters.hwpx_converter import extract_hwpx_text
from app.services.converters.pdf_converter import extract_pdf_text


@dataclass(frozen=True)
class ConvertResult:
    source_format: str
    output_type: str
    html: str | None
    text: str
    page_count: int | None
    warnings: list[str]


def _text_to_basic_html(text: str) -> str:
    escaped = html.escape(text)
    # Minimal HTML: preserve line breaks.
    return "<pre>" + escaped + "</pre>"


def convert_document(file_path: Path, source_format: str) -> ConvertResult:
    fmt = source_format.lower()

    warnings: list[str] = []
    page_count: int | None = None

    if fmt == "docx":
        text = extract_docx_text(file_path)
        return ConvertResult(
            source_format=fmt,
            output_type="html",
            html=_text_to_basic_html(text),
            text=text,
            page_count=None,
            warnings=warnings,
        )

    if fmt == "pdf":
        text, page_count = extract_pdf_text(file_path)
        warnings.append("PDF 변환은 현재 텍스트 추출 중심(MVP)입니다.")
        return ConvertResult(
            source_format=fmt,
            output_type="html",
            html=_text_to_basic_html(text),
            text=text,
            page_count=page_count,
            warnings=warnings,
        )

    if fmt == "hwpx":
        text = extract_hwpx_text(file_path)
        warnings.append("HWPX 변환은 현재 텍스트 추출 중심(MVP)입니다.")
        return ConvertResult(
            source_format=fmt,
            output_type="html",
            html=_text_to_basic_html(text),
            text=text,
            page_count=None,
            warnings=warnings,
        )

    if fmt == "hwp":
        text = extract_hwp_text(file_path)
        warnings.append("HWP 변환은 현재 텍스트 추출 중심(MVP)입니다.")
        return ConvertResult(
            source_format=fmt,
            output_type="html",
            html=_text_to_basic_html(text),
            text=text,
            page_count=None,
            warnings=warnings,
        )

    if fmt in {"doc"}:
        raise ValueError(f"Unsupported converter for: {fmt}")

    raise ValueError(f"Unknown format: {fmt}")
