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
COPY dist/frontend /app/public

# Entrypoint
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]