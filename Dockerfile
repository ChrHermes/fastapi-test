# ---------- Stage 1: Frontend ----------
FROM node:23.11-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/ ./
RUN npm install
RUN npm run build

# ---------- Stage 2: Final Image ----------
FROM python:3.12-alpine

WORKDIR /app

# Nur pip & Python
RUN apk add --no-cache py3-pip

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend kopieren und .pyc erzeugen
COPY app/ ./app
RUN python -m compileall -b app && find app -name "*.py" -delete

# Frontend einbinden (statisch)
COPY --from=frontend-builder /frontend/.output/public /app/public

# Entrypoint
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
