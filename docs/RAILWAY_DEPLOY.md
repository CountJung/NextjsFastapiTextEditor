# Railway 배포 가이드 (GitHub 연동)

이 레포는 **프론트/백 분리(모노레포)** 구조입니다. Railway에서는 보통 **서비스 2개(Frontend/Backend)** 를 만들어 각각 다른 Root Directory를 지정해 배포합니다.

## 1) 준비

- GitHub에 레포 푸시
- Railway에서 New Project → Deploy from GitHub Repo

## 2) Backend 서비스 생성 (FastAPI)

권장: Dockerfile 기반 배포(리눅스에서 `pyhwp`/`hwp5txt` 사용 가능)

- Root Directory: `web-editor-backend/`
- Build: Dockerfile 자동 감지
- Start: Dockerfile CMD가 `PORT`를 자동으로 사용

문제 해결 팁(자주 발생)

- 빌드 로그에 `start.sh not found` / `could not determine how to build`가 보이면,
  Railway 서비스의 **Root Directory가 repo 루트로 잡혀있는지** 확인하세요.
  - 해결 1(권장): Root Directory를 `web-editor-backend/`로 설정
  - 해결 2: repo 루트의 `Dockerfile`을 사용(모노레포용). 이 경우 backend 서비스는 `TARGET=backend`(기본값).

필수 환경변수(예시)

- `MAX_UPLOAD_MB=20`
- `CORS_ALLOW_ORIGINS=https://<your-frontend>.up.railway.app`

확인

- `GET https://<your-backend>.up.railway.app/api/health`

## 3) Frontend 서비스 생성 (Next.js)

- Root Directory: `web-editor-frontend/`
- Build: Dockerfile 자동 감지

필수 환경변수(중요)

- `NEXT_PUBLIC_API_BASE_URL=https://<your-backend>.up.railway.app`

참고

- `NEXT_PUBLIC_*` 값은 Next 빌드 시점에 주입될 수 있으므로, Railway에서 env 변경 후 재배포가 필요할 수 있습니다.

문제 해결 팁(자주 발생)

- 빌드 로그에 `start.sh not found` / `could not determine how to build`가 보이면,
  Root Directory가 `web-editor-frontend/`로 설정되어 있는지 확인하세요.
  - repo 루트 `Dockerfile`을 쓰는 경우, frontend 서비스는 `TARGET=frontend` 빌드 설정이 필요합니다.

## 4) HWP 지원(리눅스)

- 백엔드 컨테이너는 `pyhwp`를 포함하며, Linux에서 `hwp5txt` CLI로 HWP 텍스트 추출을 시도합니다.
- 변환 품질은 “텍스트 우선(MVP)”이므로 표/이미지 등은 누락될 수 있습니다.
