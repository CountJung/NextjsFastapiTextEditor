# NextjsFastapiTextEditor

Frontend(Next.js) / Backend(FastAPI) 분리 구조의 로컬 개발 + Docker 배포용 베이스 레포입니다.

GitHub에 게시(공개/비공개 모두)해도 CI/도커/로컬 실행에 무리가 없도록 구성되어 있습니다.

## 폴더 구조

- `web-editor-frontend/`: Next.js(TypeScript) + MUI + TipTap
- `web-editor-backend/`: FastAPI(Python) + 문서 변환(텍스트 우선, HTML 보조)

## 로컬 실행(권장)

### Backend

```powershell
cd web-editor-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

확인: `http://localhost:8000/api/health`

### Frontend

```powershell
cd web-editor-frontend
copy .env.example .env.local
npm install
npm run dev
```

확인: `http://localhost:3000`

참고: 개발 환경에서 3000 포트가 사용 중이면 Next.js가 3001로 자동 변경될 수 있습니다.

## GitHub 게시/배포(요약)

- CI: PR/Push 시 `frontend-ci`, `backend-ci`가 자동 실행됩니다.
- Docker 이미지: `main` 브랜치 push 시 GHCR로 이미지를 푸시합니다.
	- `ghcr.io/<OWNER>/<REPO>/web-editor-backend:latest`
	- `ghcr.io/<OWNER>/<REPO>/web-editor-frontend:latest`

자세한 절차는 [docs/GITHUB_PUBLISH.md](docs/GITHUB_PUBLISH.md) 참고.

## Docker Compose

```powershell
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000/api/health`

## 빠른 검증 체크리스트

1) Backend health

- `GET http://localhost:8000/api/health` → `{"ok": true, ...}`

2) Convert API (예: docx/pdf)

- Postman/curl로 `POST /api/convert`에 `multipart/form-data`로 `file` 업로드
- 응답의 `data.output.html`을 프론트가 sanitize 후 TipTap에 로드

3) Frontend UI

- `http://localhost:3000`에서 파일 선택 → 변환 → 에디터에 내용 표시
- 우측 상단 버튼으로 테마(system/light/dark) 순환 및 localStorage 저장 확인

