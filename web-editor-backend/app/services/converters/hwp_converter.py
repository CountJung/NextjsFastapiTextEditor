from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def extract_hwp_text(file_path: Path) -> str:
    """Extract text from HWP using open-source tooling.

    Current target: Linux + pyhwp (provides the `hwp5txt` CLI).
    On unsupported platforms (or when the tool is missing), raise ValueError so
    the API returns a 501 envelope.
    """

    if os.name != "posix":
        raise ValueError(
            "HWP converter requires Linux + pyhwp (hwp5txt). Not available on this platform."
        )

    exe = shutil.which("hwp5txt")
    if not exe:
        raise ValueError(
            "HWP converter requires pyhwp (hwp5txt). Install with: pip install pyhwp"
        )

    # No shell=True; capture stdout text.
    proc = subprocess.run(
        [exe, str(file_path)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    out = (proc.stdout or "").strip()
    if out:
        return out

    err = (proc.stderr or "").strip()
    raise ValueError(f"HWP conversion failed: {err or 'no output'}")
