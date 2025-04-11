#!/bin/bash

#########################################
#            Farbdefinitionen           #
#########################################

YELLOW='\033[0;33m'
RESET='\033[0m'
URL_COLOR='\033[38;2;79;163;255m'

#########################################
#         Standardparameter & Flags     #
#########################################

MIN_MB=18
MAX_MB=36
BUILD_ENABLED=false
CLEAN_ENABLED=true
CLEAN_ONLY=false
DB_PATH="./data/gcn.db"
LOG_ALL=false

#########################################
#               Funktionen              #
#########################################

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
  --log-all          Zeigt Logs aller Container (statt nur 'gc-admin')
  --help             Zeigt diese Hilfe an

Tastaturbefehle während Laufzeit:
  r   Nur App-Container + Dummy-Datenbank neu bauen
  t   Kompletter Neustart (inkl. Datenbank)
  q   Sauber beenden und Umgebung herunterfahren
"
    exit 0
}

#########################################
#          Argumente verarbeiten        #
#########################################

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
        --log-all)
            LOG_ALL=true
            shift
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
#         Dummy-Datenbank erstellen     #
#########################################

create_dummy_db() {
    if [[ -f "$DB_PATH" ]]; then
        info "Vorhandene Dummy-Datenbank wird entfernt: $DB_PATH"
        rm -f "$DB_PATH"
    fi

    SIZE_MB=$((RANDOM % (MAX_MB - MIN_MB + 1) + MIN_MB))
    EXTRA_KB=$((RANDOM % 1024))
    SIZE_KB=$((SIZE_MB * 1024 + EXTRA_KB))

    info "Erstelle Dummy-Datenbankdatei mit zufälliger Größe von ${SIZE_MB} MB + ${EXTRA_KB} kB (${SIZE_KB} kB)..."
    dd if=/dev/zero of="$DB_PATH" bs=1K count=$SIZE_KB status=none

    ACTUAL_SIZE=$(du -h "$DB_PATH" | cut -f1)
    info "Tatsächliche Größe der Datei: ${ACTUAL_SIZE}"
}

#########################################
#           Docker starten              #
#########################################

start_docker() {
    info "Starte Docker-Container...\n"
    if [ "$BUILD_ENABLED" = true ]; then
        docker-compose up --build -d
    else
        docker-compose up -d
    fi

    show_image_stats

    END_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    info "Startzeit: ${START_TIME}"
    info "Endzeit:   ${END_TIME} (Dauer: ${SECONDS}s)"
}

show_image_stats() {
    APP_CONTAINER_NAME="gc-admin"  # ggf. anpassen
    IMAGE_ID=$(docker inspect --format='{{.Image}}' "${APP_CONTAINER_NAME}" 2>/dev/null || echo "")
    
    if [[ -z "$IMAGE_ID" ]]; then
        info "Konnte Image-ID für Container '${APP_CONTAINER_NAME}' nicht ermitteln."
        return
    fi

    IMAGE_SIZE=$(docker image inspect "$IMAGE_ID" --format='{{.Size}}' 2>/dev/null || echo "")
    LAYER_COUNT=$(docker image inspect "$IMAGE_ID" --format='{{len .RootFS.Layers}}' 2>/dev/null || echo "n/a")

    if [[ -n "$IMAGE_SIZE" ]]; then
        SIZE_MB=$(echo "scale=2; $IMAGE_SIZE / 1024 / 1024" | bc)
        info "Image-Größe für '${APP_CONTAINER_NAME}': ${SIZE_MB} MB"
        info "Anzahl Layer: ${LAYER_COUNT}"
    else
        info "Konnte Image-Infos für '${APP_CONTAINER_NAME}' nicht ermitteln."
    fi
}

show_logs() {
    info "Server läuft auf ${URL_COLOR}http://127.0.0.1:8000${RESET}"
    info "Docker-Logs werden angezeigt.\n       ('r' = App-Container neustarten, 't' = kompletter Neustart, 'q' = Beenden.)"
    
    if [ "$LOG_ALL" = true ]; then
        docker-compose logs -f &
    else
        docker-compose logs -f gc-admin &
    fi
    LOG_PID=$!
}

stop_docker() {
    info "Beende Docker-Container..."
    docker-compose down --remove-orphans
    if [ "$CLEAN_ENABLED" = true ]; then
        info "Entferne Datenbankdatei..."
        rm -f "$DB_PATH"*
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
    APP_CONTAINER_NAME="gc-admin"
    info "Dummy-Datenbank wird neu erstellt..."
    create_dummy_db
    info "Baue und starte nur den Container '${APP_CONTAINER_NAME}' neu..."
    docker-compose build "$APP_CONTAINER_NAME"
    docker-compose up -d --no-deps --force-recreate "$APP_CONTAINER_NAME"
}

cleanup() {
    kill $LOG_PID 2>/dev/null
    stop_docker
    exit 0
}

#########################################
#          Signal-Handler setzen        #
#########################################

trap cleanup SIGINT SIGTERM

#########################################
#            Nur Cleanup-Modus          #
#########################################

if [ "$CLEAN_ONLY" = true ]; then
    info "Nur-Cleanup-Modus aktiviert (--clean-only)"
    CLEAN_ENABLED=true
    stop_docker
    exit 0
fi

#########################################
#               Hauptablauf             #
#########################################

START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
SECONDS=0

create_dummy_db
start_docker
show_logs

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
