#!/bin/bash

# Farbdefinitionen
YELLOW='\033[0;33m'
RESET='\033[0m'
URL_COLOR='\033[38;2;79;163;255m'

# Standardgrenzen für Dummy-Datenbank (in MB)
MIN_MB=18
MAX_MB=36

# Flags
BUILD_ENABLED=false
CLEAN_ENABLED=true
CLEAN_ONLY=false

info() {
    printf "\n${YELLOW}[INFO] $1${RESET}\n"
}

show_help() {
    echo -e "
Verfügbare Optionen:
  --build            Führe docker-compose mit --build aus
  --clean-only       Führt nur das Entfernen der Datenbankdatei aus
  --no-clean         Lässt Datenbankdatei beim Beenden bestehen
  --min <MB>         Minimale Größe der Dummy-Datenbank
  --max <MB>         Maximale Größe der Dummy-Datenbank
  --help             Zeigt diese Hilfe an

Tastaturbefehle während Laufzeit:
  r   Nur App-Container neu bauen und starten
  t   Kompletter Neustart (inkl. Datenbank)
  q   Sauber beenden und Umgebung herunterfahren
"
    exit 0
}

# Argumente verarbeiten
while [[ $# -gt 0 ]]; do
    case "$1" in
        --build)
            BUILD_ENABLED=true
            shift
            ;;
        --no-clean)
            CLEAN_ENABLED=false
            shift
            ;;
        --clean-only)
            CLEAN_ONLY=true
            shift
            ;;
        --min)
            MIN_MB="$2"
            shift 2
            ;;
        --max)
            MAX_MB="$2"
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

create_dummy_db() {
    SIZE_MB=$((RANDOM % (MAX_MB - MIN_MB + 1) + MIN_MB))
    EXTRA_KB=$((RANDOM % 1024))
    SIZE_KB=$((SIZE_MB * 1024 + EXTRA_KB))

    info "Erstelle Dummy-Datenbankdatei mit zufälliger Größe von ${SIZE_MB} MB + ${EXTRA_KB} kB (${SIZE_KB} kB)..."
    dd if=/dev/zero of=./data/gcn.db bs=1K count=$SIZE_KB status=none

    ACTUAL_SIZE=$(du -h ./data/gcn.db | cut -f1)
    info "Tatsächliche Größe der Datei: ${ACTUAL_SIZE}"
}

start_docker() {
    info "Starte Docker-Container..."
    if [ "$BUILD_ENABLED" = true ]; then
        docker-compose up --build -d
    else
        docker-compose up -d
    fi
}

show_logs() {
    info "Server läuft auf ${URL_COLOR}http://127.0.0.1:8080${RESET}"
    info "Docker-Logs werden angezeigt. 'r' = App-Container neustarten, 't' = kompletter Neustart, 'q' = Beenden."
    docker-compose logs -f &
    LOG_PID=$!
}

stop_docker() {
    info "Beende Docker-Container..."
    docker-compose down --remove-orphans
    if [ "$CLEAN_ENABLED" = true ]; then
        info "Entferne Datenbankdatei..."
        rm -f ./data/gcn.db*
    else
        info "Cleanup deaktiviert (--no-clean gesetzt)"
    fi
}

restart() {
    info "Neustart ausgelöst."
    kill $LOG_PID
    stop_docker
    create_dummy_db
    start_docker
    show_logs
}

rebuild_app_container() {
    APP_CONTAINER_NAME="app"  # ggf. anpassen an deinen Compose-Dienstnamen
    info "Baue und starte nur den Container '${APP_CONTAINER_NAME}' neu..."
    docker-compose build "$APP_CONTAINER_NAME"
    docker-compose up -d --no-deps --force-recreate "$APP_CONTAINER_NAME"
}

cleanup() {
    kill $LOG_PID 2>/dev/null
    stop_docker
    exit 0
}

trap cleanup SIGINT SIGTERM

# Nur Cleanup-Modus
if [ "$CLEAN_ONLY" = true ]; then
    info "Nur-Cleanup-Modus aktiviert (--clean-only)"
    CLEAN_ENABLED=true
    stop_docker
    exit 0
fi

# Ablauf starten
create_dummy_db
start_docker
show_logs

# Tasteneingaben auswerten
while true; do
    read -rsn1 key
    case "$key" in
        r|R)
            rebuild_app_container
            ;;
        t|T)
            restart
            ;;
        q|Q)
            cleanup
            ;;
    esac
done
