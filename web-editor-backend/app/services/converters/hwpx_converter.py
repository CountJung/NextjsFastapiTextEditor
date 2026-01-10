from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def extract_hwpx_text(file_path: Path) -> str:
    """Best-effort HWPX text extraction.

    HWPX is a zip container with XML parts. We keep this intentionally simple and
    extract readable text by concatenating XML text nodes.
    """

    texts: list[str] = []

    with zipfile.ZipFile(file_path) as zf:
        # Most HWPX content is under Contents/*.xml; we try all XML files there.
        candidates = [
            name
            for name in zf.namelist()
            if name.lower().startswith("contents/") and name.lower().endswith(".xml")
        ]
        for name in sorted(candidates):
            data = zf.read(name)
            try:
                root = ET.fromstring(data)
            except ET.ParseError:
                continue
            for node_text in root.itertext():
                s = (node_text or "").strip()
                if s:
                    texts.append(s)

    return "\n".join(texts).strip()
