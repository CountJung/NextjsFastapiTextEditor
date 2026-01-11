# Root Dockerfile for Railway monorepo deployments.
#
# Railway sometimes deploys from repo root; without a root-level Dockerfile it may
# fail to detect how to build (e.g. complaining about missing start.sh).
#
# Use build args:
# - TARGET=backend|frontend (default backend)
# - INSTALL_HWP=1|0 (backend only; default 1)
# - NEXT_PUBLIC_API_BASE_URL (frontend build-time env)

ARG TARGET=backend

############################
# Backend runtime image
############################
FROM python:3.11-slim AS backend

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG INSTALL_HWP=1

COPY web-editor-backend/pyproject.toml /app/pyproject.toml

RUN pip install --no-cache-dir -U pip \
  && if [ "$INSTALL_HWP" = "1" ]; then \
       pip install --no-cache-dir ".[hwp]"; \
     else \
       pip install --no-cache-dir .; \
     fi

COPY web-editor-backend/app /app/app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

############################
# Frontend runtime image
############################
FROM node:20-alpine AS frontend

WORKDIR /app

# Build-time public env for Next.js (baked into the client bundle).
ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

COPY web-editor-frontend/package.json web-editor-frontend/package-lock.json ./
RUN npm ci

COPY web-editor-frontend/ ./
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]

############################
# Final stage selection
############################
ARG TARGET=backend
FROM ${TARGET} AS final
