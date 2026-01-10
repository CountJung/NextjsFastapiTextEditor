import io

from fastapi.testclient import TestClient

from app.main import app


def test_convert_rejects_unknown_ext() -> None:
    client = TestClient(app)
    res = client.post(
        "/api/convert",
        files={"file": ("malware.exe", io.BytesIO(b"x"), "application/octet-stream")},
    )
    assert res.status_code == 400
    body = res.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "UNSUPPORTED_FILE_TYPE"
