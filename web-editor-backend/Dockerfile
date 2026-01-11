FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1 = install HWP support (pyhwp/hwp5txt). Keep it on by default for NAS/Linux usage.
ARG INSTALL_HWP=1

COPY pyproject.toml /app/pyproject.toml

RUN pip install --no-cache-dir -U pip \
  && if [ "$INSTALL_HWP" = "1" ]; then \
       pip install --no-cache-dir ".[hwp]"; \
     else \
       pip install --no-cache-dir .; \
     fi

COPY app /app/app

EXPOSE 8000

# Railway sets $PORT; default to 8000 locally.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
