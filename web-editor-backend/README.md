# web-editor-backend

FastAPI 기반 문서 변환 백엔드(MVP)입니다.

## 엔드포인트

- `GET /api/health`
- `POST /api/convert` (multipart/form-data, field: `file`)

## 환경변수

- `CORS_ALLOW_ORIGINS`: 예) `http://localhost:3000`
- `MAX_UPLOAD_MB`: 업로드 최대 크기(MB), 기본 20
