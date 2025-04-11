#!/bin/bash

#########################################
#            Farbdefinitionen           #
#########################################

YELLOW='\033[0;33m'
RESET='\033[0m'

#########################################
#         Skript-Optionen & Flags       #
#########################################

set -e

VENV_DIR=".venv"
CLEAN_ENABLED=true
CLEAN_ONLY=false
INSTALL_REQUIREMENTS=false
FRONTEND_DIR="frontend"

#########################################
#               Funktionen              #
#########################################

info() {
    printf "\n${YELLOW}[INFO] $1${RESET}\n"
}

show_help() {
    echo -e "
Verfügbare Optionen:
  --venv <pfad>     Pfad zur virtuellen Umgebung (Standard: .venv)
  --install         Installiert die Python-Abhängigkeiten
  --no-clean        Lässt __pycache__ beim Beenden bestehen
  --clean-only      Führt nur das Entfernen von __pycache__ aus
  --help            Zeigt diese Hilfe an
"
    exit 0
}

cleanup_pycache() {
    if [ "$CLEAN_ENABLED" = true ]; then
        info "🧹 Entferne __pycache__-Ordner unter app/..."
        find app/ -type d -name "__pycache__" -exec rm -r {} +
    fi
}

on_interrupt() {
    info "⛔️ Entwicklung wurde beendet (Strg+C)"
    cleanup_pycache
    exit 0
}

#########################################
#          Argumente parsen             #
#########################################

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-clean)
            CLEAN_ENABLED=false
            shift
            ;;
        --clean-only)
            CLEAN_ONLY=true
            shift
            ;;
        --install)
            INSTALL_REQUIREMENTS=true
            shift
            ;;
        --venv)
            VENV_DIR="$2"
            shift 2
            ;;
        --help)
            show_help
            ;;
        *)
            echo "Unbekannte Option: $1"
            show_help
            ;;
    esac
done

#########################################
#            Nur Cleanup-Modus          #
#########################################

if [ "$CLEAN_ONLY" = true ]; then
    cleanup_pycache
    exit 0
fi

trap on_interrupt SIGINT

#########################################
#  Virtuelle Umgebung aktivieren        #
#########################################

if [[ ! -d "$VENV_DIR" ]]; then
    info "⚠️  Virtuelle Umgebung nicht gefunden: $VENV_DIR"
    echo "👉 Bitte zuerst: python -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source "$VENV_DIR/bin/activate"

if [ "$INSTALL_REQUIREMENTS" = true ]; then
    info "📦 Installiere Python-Abhängigkeiten..."
    pip install -r requirements.txt
fi

#########################################
#     Backend & Frontend starten        #
#########################################

info "🚀 Starte Entwicklungssystem..."

# Start backend im Hintergrund
uvicorn app.main:app --reload &
BACKEND_PID=$!

# Frontend starten (eigenes Terminalfenster öffnet meist automatisch Nuxt UI)
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
cd -

# Warten auf Prozesse
wait $BACKEND_PID $FRONTEND_PID
