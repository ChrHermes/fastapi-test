#!/bin/bash

# Farbdefinitionen
YELLOW='\033[0;33m'
RESET='\033[0m'

# Sofort abbrechen bei Fehlern
set -e

# Pfad zur virtuellen Umgebung
VENV_DIR=".venv"

# Flags
CLEAN_ENABLED=true
CLEAN_ONLY=false
INSTALL_REQUIREMENTS=false

# Argumente parsen
for arg in "$@"; do
    case "$arg" in
        --no-clean)
            CLEAN_ENABLED=false
            ;;
        --clean-only)
            CLEAN_ONLY=true
            ;;
        --install)
            INSTALL_REQUIREMENTS=true
            ;;
        --help)
            show_help
            ;;
    esac
done

info() {
    printf "\n${YELLOW}[INFO] $1${RESET}\n"
}

show_help() {
    echo -e "
Verfügbare Optionen:
  --install         Installiert die Abhängigkeiten aus requirements.txt in der virtuellen Umgebung
  --no-clean        Lässt __pycache__ beim Beenden bestehen
  --clean-only      Führt nur das Entfernen von __pycache__-Ordnern unter app/ aus
  --help            Zeigt diese Hilfe an
"
    exit 0
}

cleanup_pycache() {
    if [ "$CLEAN_ENABLED" = true ]; then
        info "Entferne __pycache__-Ordner unter app/..."
        find app/ -type d -name "__pycache__" -exec rm -r {} +
    else
        info "Cleanup deaktiviert (--no-clean gesetzt)"
    fi
}

on_interrupt() {
    info "Uvicorn wurde abgebrochen (Strg+C)"
    cleanup_pycache
    exit 0
}

# Nur Cleanup-Modus
if [ "$CLEAN_ONLY" = true ]; then
    cleanup_pycache
    exit 0
fi

# Trap für Strg+C (SIGINT)
trap on_interrupt SIGINT

# Prüfen, ob die virtuelle Umgebung existiert
if [[ ! -d "$VENV_DIR" ]]; then
    info "Virtuelle Umgebung nicht gefunden: $VENV_DIR"
    info "Bitte zuerst: python -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Aktivieren der virtuellen Umgebung
source "$VENV_DIR/bin/activate"

if [ "$INSTALL_REQUIREMENTS" = true ]; then
    info "Installiere Python-Abhängigkeiten aus requirements.txt..."
    pip install -r requirements.txt
fi

# Uvicorn starten
info "Starte Uvicorn mit automatischem Reload..."
uvicorn app.main:app --reload
