# GitHub 게시 & 운영 가이드

이 문서는 이 레포를 GitHub에 게시한 뒤, CI로 품질을 유지하고 GHCR 이미지로 배포하는 기본 흐름을 정리합니다.

## 1) GitHub Actions(CI)

- Frontend: `.github/workflows/frontend-ci.yml`
- Backend: `.github/workflows/backend-ci.yml`

PR/Push 시 자동으로 빌드/테스트가 수행됩니다.

## 2) GHCR(Docker 이미지) 자동 푸시

워크플로: `.github/workflows/docker-ghcr.yml`

- 트리거: 수동 실행(workflow_dispatch)
- 푸시되는 태그:
  - `ghcr.io/<OWNER>/<REPO>/web-editor-backend:latest`
  - `ghcr.io/<OWNER>/<REPO>/web-editor-frontend:latest`

참고:
- `GITHUB_TOKEN`을 사용해 GHCR에 푸시합니다(추가 시크릿 없이 동작).
- 레포가 **public**인 경우, 패키지 가시성은 GitHub Packages 설정에서 조정할 수 있습니다.

## 3) NAS(시놀로지)에서 실행

개념적으로는 아래 흐름입니다.

1) NAS에서 `docker login ghcr.io`
2) compose 파일에서 이미지 이름을 GHCR로 지정
3) `docker compose pull` 후 `docker compose up -d`

또는, GHCR을 쓰지 않고 NAS에서 직접 `docker compose up -d --build`로 빌드/실행할 수도 있습니다.

환경변수 예시:

- backend
  - `CORS_ALLOW_ORIGINS=http://<NAS-DOMAIN>:3001`
- frontend
  - `NEXT_PUBLIC_API_BASE_URL=http://<NAS-DOMAIN>:8000`

### HWP 변환(리눅스 컨테이너)

- 백엔드 Docker 이미지는 기본적으로 `pyhwp`를 포함하도록 구성되어 있습니다.
- 실제 HWP 변환은 Linux에서 `hwp5txt` CLI를 호출해 텍스트를 추출합니다.
- Windows 로컬에서는 HWP 변환이 동작하지 않으며(의도된 제한), API는 `501 NOT_IMPLEMENTED` envelope로 응답합니다.

## 4) 로컬에서 확인

- backend: `http://localhost:8000/api/health`
- frontend: `http://localhost:3001`
