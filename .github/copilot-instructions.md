# Copilot Instructions (NextjsFastapiTextEditor)

## Big picture
- Monorepo with two deployable services:
  - Frontend: `web-editor-frontend/` (Next.js App Router + MUI + TipTap)
  - Backend: `web-editor-backend/` (FastAPI + document conversion “text-first”)
- Data flow: Frontend uploads a file → Backend converts → Backend returns an **enveloped** JSON response → Frontend sanitizes HTML → TipTap loads content.

## Backend conventions (FastAPI)
- Entrypoint: `web-editor-backend/app/main.py`.
- API response format is always the envelope `{ ok, data, error }`.
  - For non-2xx, **do not** throw `HTTPException(detail=...)` if you want the envelope at top-level; set `response.status_code` and return `Envelope` (see `/api/convert`).
- Upload handling: stream `UploadFile` to a temp file with size limit (`MAX_UPLOAD_MB`, default 20), then delete temp file in `finally`.
- Allowed extensions: `pdf/doc/docx/hwp/hwpx`.
  - MVP converters implemented: `docx`, `pdf`.
  - `hwpx`: zip+xml 기반 best-effort 텍스트 추출.
  - `hwp`: Linux 컨테이너에서 `pyhwp`의 `hwp5txt`를 호출해 텍스트 추출.
  - `doc`는 `501 NOT_IMPLEMENTED` (see `app/services/convert_service.py`).
- Add/extend converters under `web-editor-backend/app/services/converters/` and wire them in `convert_service.convert_document`.

## Frontend conventions (Next.js + MUI + TipTap)
- Upload → convert flow lives in `web-editor-frontend/src/components/UploadConvert.tsx`.
- API client uses `NEXT_PUBLIC_API_BASE_URL` and expects the envelope (see `src/lib/api.ts`).
- Always sanitize backend HTML before rendering/importing into editor (`src/lib/sanitizeHtml.ts`).
- Theme mode is `system/light/dark` stored in localStorage and propagated via `themeModeChanged` window event (`ThemeModeToggle.tsx`, `useAppTheme.ts`).

## Dev workflows (local)
- Backend (Windows): `cd web-editor-backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -e .[dev]; uvicorn app.main:app --reload`.
- Frontend: `cd web-editor-frontend; npm ci; npm run dev -- --port 3001` (기본 포트 3001 고정).
- VS Code run/debug is preconfigured in `.vscode/launch.json` and `.vscode/tasks.json` (compound: “Dev: Frontend + Backend”).
- Backend smoke test against a running server: `web-editor-backend/scripts/smoke_convert.py`.

## CI/CD (GitHub)
- CI: `.github/workflows/frontend-ci.yml` (npm ci + build) and `.github/workflows/backend-ci.yml` (ruff + pytest).
- Deploy: Railway에서 GitHub 연동 후 push 감지로 자동 배포(모노레포라 서비스 2개로 분리 권장).

## What not to assume
- HWP/HWPX 변환은 오픈소스 기반으로 단계적으로 구현 중입니다.
  - HWP: Linux에서 `pyhwp`(hwp5txt) 기반 텍스트 추출을 우선 고려
  - HWPX: zip+xml 기반 best-effort 텍스트 추출부터 시작
