
# BUILD_PLAN.md — 웹 워드 문서 편집기 (Frontend/Backend 분리) Copilot 기반 빌드 플랜

- Current Date: 2026-01-10
- Current user's login: CountJung
- 목표: GitHub Copilot을 활용해 **Frontend(Next.js) / Backend(FastAPI)** 분리 레포 구조로 “리치 텍스트 편집 + 문서 변환” 서비스를 **로컬/CI/도커(시놀로지 NAS)** 환경에서 재현 가능하게 빌드한다.

추가 방향(2026-01-10): GitHub에 게시(공개/비공개) 후에도 바로 동작하도록 CI/GHCR 기반 배포 루트를 포함한다.

---

## 0) 결정사항(사용자 확정 반영)

1. 레포지토리 형태: **프론트 / 백엔드 분리(2개 레포 또는 2개 폴더-분리 운영 전제)**
2. 편집기 종류: **리치 텍스트 에디터 기반**
3. HWP/HWPX: **오픈소스 기반 변환 목표**
4. 배포: **시놀로지 NAS → Docker/Compose 형태**가 적합

---

## 1) 최종 아키텍처(권장)

### 1.1 구성
- Frontend Repo: Next.js(TypeScript) + MUI + Theme mode(system/dark/light) + Rich Text Editor
- Backend Repo: FastAPI(Python) + 문서 변환 파이프라인 + 파일 업로드 API
- 배포: Synology NAS의 Docker/Container Manager에서 `docker-compose.yml`로 구동

### 1.2 통신 원칙(API 우선)
- Frontend ↔ Backend: REST API(JSON) + 파일 업로드는 `multipart/form-data`
- 장시간 변환 대비(2단계 확장):
  - 1차(MVP): 동기 변환(요청→응답)
  - 2차: 비동기 Job(요청→jobId→상태조회/결과조회)

---

## 2) 레포지토리 구조(분리 레포 권장)

### 2.1 Frontend Repo (예: `web-editor-frontend`)
```text
web-editor-frontend/
  src/
  public/
  next.config.*
  package.json
  tsconfig.json
  README.md
  .env.example
  Dockerfile
```

### 2.2 Backend Repo (예: `web-editor-backend`)

```text
web-editor-backend/
  app/
    main.py
    api/
    services/
    converters/
  tests/
  pyproject.toml (또는 requirements.txt)
  README.md
  .env.example
  Dockerfile
```

---

## 3) 기술 스택 상세(권장 선택)

## 3.1 Frontend

- Next.js (권장: 최신 stable, App Router 사용 여부는 팀 선택)
- TypeScript
- MUI
- Theme mode: `system/dark/light`
- Rich Text Editor(권장 후보)
  - **TipTap(ProseMirror 기반)**: 확장성 좋고 Next.js 친화적
  - 대안: Slate, Quill(구현 단순), Lexical(메타)

> 권장: “변환 결과를 HTML로 받는 방식” + TipTap에 HTML import/렌더 적용

## 3.2 Backend

- Python 3.11+
- FastAPI + Uvicorn
- 변환 라이브러리/도구 후보(오픈소스 기반)
  - DOCX: `python-docx` / `docx2txt`
  - PDF: `pymupdf` 또는 `pdfplumber`
  - HWP/HWPX: 오픈소스 도구/라이브러리 검증 필요(정확도/지원 범위 편차 큼)
  - 공통 변환: `pandoc`(지원 범위 확인 필요)
  - (옵션) LibreOffice headless: 오픈소스이지만 이미지가 커지고 폰트/환경 이슈 존재

> HWP/HWPX는 “완벽 변환”보다 “텍스트 추출/단순 구조 유지”를 목표로 단계적 고도화 권장

---

## 4) API 계약(최소 빌드/연동 기준)

### 4.1 공통 응답 포맷(envelope 권장)

```json
{
  "ok": true,
  "data": {},
  "error": null
}
```

### 4.2 필수 엔드포인트(MVP)

#### (1) Health Check

- `GET /api/health`
- Response:

```json
{ "ok": true, "data": { "status": "up" }, "error": null }
```

#### (2) Convert (동기)

- `POST /api/convert`
- Content-Type: `multipart/form-data`
- Form field: `file`
- Response(예시):

```json
{
  "ok": true,
  "data": {
    "sourceFormat": "docx",
    "output": {
      "type": "html",
      "html": "<p>...</p>",
      "text": "..."
    },
    "metadata": {
      "pageCount": null
    },
    "warnings": []
  },
  "error": null
}
```

> Frontend는 우선 `output.type=html`을 에디터에 로드하고, 실패 시 `text` fallback 표시

---

## 5) Copilot 활용 운영 가이드(실행 중심)

### 5.1 Copilot에 제공할 “고정 컨텍스트”

- API 스펙(요청/응답 JSON)
- 파일 업로드 제한(확장자, MIME, 사이즈)
- 변환 목표(HTML 우선, text fallback)
- Synology Docker 배포(환경변수/포트/CORS)

### 5.2 추천 프롬프트 템플릿

#### Backend(예시)

- “FastAPI로 `/api/convert` 구현. 입력 multipart file. 확장자(pdf/doc/docx/hwp/hwpx) 허용. 결과는 HTML 우선 + text fallback. 실패 시 `{code, message, details}` 구조로 error 내려줘. 임시파일 저장 후 변환하고 삭제.”

#### Frontend(예시)

- “Next.js+MUI로 업로드→변환→TipTap 에디터에 HTML 주입 흐름 구현. 로딩/오류/진행 표시. theme mode(system/dark/light) 토글 및 localStorage 저장.”

---

## 6) 빌드 플로우(로컬 개발)

## 6.1 Backend 로컬 실행

- Python venv 생성 및 의존성 설치
- 실행:
  - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- 점검:
  - `GET http://localhost:8000/api/health`

## 6.2 Frontend 로컬 실행

- Node LTS 설치
- `.env.local`에 백엔드 주소 설정:
  - 예: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
- 실행:
  - `npm install`
  - `npm run dev`
- 점검:
  - 업로드 후 변환 결과가 에디터에 표시되는지 확인

---

## 7) CI 계획(GitHub Actions) — 분리 레포 기준

## 7.1 Frontend CI

- Trigger: push / pull_request
- Jobs:
  - install
  - lint
  - typecheck
  - build

## 7.2 Backend CI

- Trigger: push / pull_request
- Jobs:
  - install
  - lint(ruff 권장)
  - test(pytest)
  - (옵션) mypy

---

## 8) Docker 배포(시놀로지 NAS 목표)

### 8.3 GitHub 게시/이미지 배포(GHCR)

- `main` 브랜치에 push 시 GHCR에 프론트/백 Docker 이미지를 자동 푸시
- Synology NAS는 해당 이미지를 pull하여 `docker-compose.yml`로 운영(환경변수로 API_BASE/CORS 제어)


## 8.1 배포 전략

- Synology NAS에서 `docker compose`로 운영
- 외부 접속은 NAS 리버스 프록시(선택) 또는 compose에서 포트 노출
- 권장 포트:
  - frontend: 3001
  - backend: 8000

## 8.2 docker-compose 예시(배포 서버에 별도 디렉토리로 관리)
>
> 실제 운영에서는 이미지 태그/레지스트리/볼륨/로그 정책을 추가

```yaml
services:
  backend:
    image: your-registry/web-editor-backend:latest
    container_name: web-editor-backend
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=prod
      - CORS_ALLOW_ORIGINS=http://your-nas-domain-or-ip:3000
    restart: unless-stopped

  frontend:
    image: your-registry/web-editor-frontend:latest
    container_name: web-editor-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://your-nas-domain-or-ip:8000
    depends_on:
      - backend
    restart: unless-stopped
```

---

## 9) 변환 파이프라인 구현 우선순위(오픈소스 기반, 리스크 포함)

### 9.1 1차(MVP)

- DOCX → HTML/text (정확도/난이도 균형 좋음)
- PDF → text(또는 HTML 유사 출력) (문서에 따라 품질 편차)

### 9.2 2차

- HWP/HWPX → text(우선) → HTML(가능 범위 내)
- 경고(warnings) 체계:
  - “표/이미지/머리말/주석은 일부 누락될 수 있음” 등을 명시

### 9.3 리스크 관리

- HWP/HWPX는 오픈소스 생태계가 제한적일 수 있어:
  - “추출 성공/실패 케이스 수집”
  - “문서 샘플 세트(테스트 fixtures) 구축”
  - “지원 범위 명시(초기에는 텍스트 중심)”가 필요

---

## 10) 프론트 리치 텍스트 에디터 요구사항(체크리스트)

- HTML Import(변환 결과 주입)
- 기본 서식: bold/italic/underline, heading, list, link
- 붙여넣기 시 sanitize(보안)
- theme mode 반영(MUI 테마 연동)
- (선택) autosave / document versioning

---

## 11) 보안/운영 체크리스트(도커/NAS 관점)

- 업로드 제한: 확장자 + MIME + 사이즈(예: 20MB)
- 임시 파일 저장 위치를 컨테이너 내부/볼륨으로 분리하고 자동 정리
- CORS 최소 허용(프론트 도메인만)
- 로그: stdout 기반 + NAS에서 로그 로테이션 정책 검토
- 변환 도구 실행 시:
  - shell=True 금지
  - 안전한 인자 전달
  - 타임아웃 설정(대용량/악성 파일 방어)

---

## 12) 다음에 확정하면 “실행 가능한” 빌드 문서로 더 구체화 가능

아래 4가지만 답해주면, 이 문서를 **각 레포별 README + Dockerfile + compose + CI** 수준까지 “명령어 단위”로 확정해 정리할 수 있다.

1. Frontend/Backend 레포 이름 -> 프로젝트 명칭은 NextjsFastapiTextEditor
2. Rich Text Editor는 TipTap 권장으로 사용
3. 변환 결과 포맷은 텍스트 우선으로 사용
4. NAS 접속 방식은 최종 리버스 프록시 사용 예정이며 env 세팅으로 처리한다.


