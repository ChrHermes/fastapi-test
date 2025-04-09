# ---------- Build Stage: Frontend ----------
FROM node:23.11-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/ ./
RUN npm install
RUN npm run build

# ---------- Final Stage: Backend ----------
FROM python:3.13-alpine

# Systemtools
RUN apk add --no-cache bash build-base

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend-Code kopieren
COPY app/ ./app

# Nuxt statisches Build-Ergebnis kopieren
COPY --from=frontend-builder /frontend/.output/public ./static

# Uvicorn starten + Static-Dateien einbinden
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
