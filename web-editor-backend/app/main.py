from __future__ import annotations

import html
import os
import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.convert_service import ConvertResult, convert_document


class ApiError(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class Envelope(BaseModel):
    ok: bool
    data: dict[str, Any] | None = None
    error: ApiError | None = None


def _parse_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


MAX_UPLOAD_MB = _parse_int_env("MAX_UPLOAD_MB", 20)
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024


app = FastAPI(title="web-editor-backend", version="0.1.0")

cors_allow_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://localhost:3001",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)


@app.get("/api/health", response_model=Envelope)
def health() -> Envelope:
    return Envelope(ok=True, data={"status": "up"}, error=None)


def _ext_from_filename(filename: str | None) -> str:
    if not filename:
        return ""
    return Path(filename).suffix.lower().lstrip(".")


ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "hwp", "hwpx"}


@app.post("/api/convert", response_model=Envelope)
async def convert(response: Response, file: UploadFile = File(...)) -> Envelope:
    ext = _ext_from_filename(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        response.status_code = 400
        return Envelope(
            ok=False,
            data=None,
            error=ApiError(
                code="UNSUPPORTED_FILE_TYPE",
                message=f"Unsupported file type: {html.escape(ext or '(none)')}",
                details={"allowed": sorted(ALLOWED_EXTENSIONS)},
            ),
        )

    # Stream to temp file with size limit.
    tmp_path: Path | None = None
    size = 0
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp_path = Path(tmp.name)
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    response.status_code = 413
                    return Envelope(
                        ok=False,
                        data=None,
                        error=ApiError(
                            code="FILE_TOO_LARGE",
                            message=f"File exceeds max upload size ({MAX_UPLOAD_MB}MB)",
                            details={"maxUploadMb": MAX_UPLOAD_MB},
                        ),
                    )
                tmp.write(chunk)

        result: ConvertResult = convert_document(tmp_path, source_format=ext)
        return Envelope(
            ok=True,
            data={
                "sourceFormat": result.source_format,
                "output": {
                    "type": result.output_type,
                    "html": result.html,
                    "text": result.text,
                },
                "metadata": {"pageCount": result.page_count},
                "warnings": result.warnings,
            },
            error=None,
        )
    except ValueError as exc:
        # Known "not implemented" formats (doc/hwp/hwpx) are allowed by extension,
        # but converter is not yet available in MVP.
        response.status_code = 501
        return Envelope(
            ok=False,
            data=None,
            error=ApiError(
                code="NOT_IMPLEMENTED",
                message=str(exc) or "Converter not implemented",
                details={"sourceFormat": ext},
            ),
        )
    except Exception as exc:
        response.status_code = 500
        return Envelope(
            ok=False,
            data=None,
            error=ApiError(
                code="CONVERT_FAILED",
                message="Conversion failed",
                details={"exception": exc.__class__.__name__},
            ),
        )
    finally:
        try:
            await file.close()
        except Exception:
            pass
        if tmp_path is not None:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
