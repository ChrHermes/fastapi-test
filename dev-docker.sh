#!/bin/bash

# Farbdefinitionen
YELLOW='\033[0;33m'
RESET='\033[0m'
URL_COLOR='\033[38;2;79;163;255m'

# Konfigurierbare Grenzwerte für Dummy-Datenbank (in MB)
MIN_MB=18
MAX_MB=36

info() {
    printf "\n${YELLOW}[INFO] $1${RESET}\n"
}

create_dummy_db() {
    # Zufällige Größe in MB und zusätzliche KB
    SIZE_MB=$((RANDOM % (MAX_MB - MIN_MB + 1) + MIN_MB))
    EXTRA_KB=$((RANDOM % 1024))
    SIZE_KB=$((SIZE_MB * 1024 + EXTRA_KB))

    info "Erstelle Dummy-Datenbankdatei mit zufälliger Größe von ${SIZE_MB} MB + ${EXTRA_KB} kB (${SIZE_KB} kB)..."

    dd if=/dev/zero of=./data/gcn.db bs=1K count=$SIZE_KB

    # Tatsächliche Dateigröße anzeigen
    ACTUAL_SIZE=$(du -h ./data/gcn.db | cut -f1)
    info "Tatsächliche Größe der Datei: ${ACTUAL_SIZE}"
}

start_docker() {
    info "Starte Docker-Container..."
    docker-compose up --build -d
}

show_logs() {
    info "Server läuft auf ${URL_COLOR}http://127.0.0.1:8080${RESET}"
    info "Docker-Logs werden angezeigt. 'r' = Neustart, 'q' = Beenden."
    docker-compose logs -f &
    LOG_PID=$!
}

stop_docker() {
    info "Beende Docker und entferne Datenbank..."
    docker-compose down --remove-orphans
    rm -f ./data/gcn.db*
}

restart() {
    info "Neustart ausgelöst."
    kill $LOG_PID
    stop_docker
    create_dummy_db
    start_docker
    show_logs
}

cleanup() {
    kill $LOG_PID 2>/dev/null
    stop_docker
    exit 0
}

trap cleanup SIGINT SIGTERM

# Ablauf starten
create_dummy_db
start_docker
show_logs

# Tasteneingaben auswerten
while true; do
    read -rsn1 key
    case "$key" in
        r|R)
            restart
            ;;
        q|Q)
            cleanup
            ;;
    esac
done
