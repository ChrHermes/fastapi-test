#!/bin/bash

#########################################
#            Farbdefinitionen           #
#########################################

YELLOW='\033[0;33m'
RESET='\033[0m'

#########################################
#         Skript-Optionen & Flags       #
#########################################

set -e  # Sofort abbrechen bei Fehlern

VENV_DIR=".venv"             # Standardpfad zur virtuellen Umgebung
CLEAN_ENABLED=true           # __pycache__ beim Beenden löschen
CLEAN_ONLY=false             # Nur Cleanup ohne Start
INSTALL_REQUIREMENTS=false   # Requirements installieren

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

#########################################
#        Signal-Handler setzen          #
#########################################

trap on_interrupt SIGINT

#########################################
#   Virtuelle Umgebung prüfen/aktivieren#
#########################################

if [[ ! -d "$VENV_DIR" ]]; then
    info "Virtuelle Umgebung nicht gefunden: $VENV_DIR"
    info "Bitte zuerst: python -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source "$VENV_DIR/bin/activate"

if [ "$INSTALL_REQUIREMENTS" = true ]; then
    info "Installiere Python-Abhängigkeiten aus requirements.txt..."
    pip install -r requirements.txt
fi

#########################################
#        Uvicorn starten                #
#########################################

info "Starte Uvicorn mit automatischem Reload..."
uvicorn app.main:app --reload
