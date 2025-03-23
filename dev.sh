#!/bin/bash

# Skript bei Fehlern sofort abbrechen
set -e

# Pfad zur virtuellen Umgebung
VENV_DIR=".venv"

# Prüfen, ob die virtuelle Umgebung existiert
if [[ ! -d "$VENV_DIR" ]]; then
    echo "⚠️  Virtuelle Umgebung nicht gefunden: $VENV_DIR"
    echo "👉  Bitte zuerst: python -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Aktivieren der virtuellen Umgebung
source "$VENV_DIR/bin/activate"

# Starte Uvicorn mit automatischem Reload
exec uvicorn app.main:app --reload
