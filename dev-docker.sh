#!/bin/bash

# Farbdefinitionen
YELLOW='\033[0;33m'
RESET='\033[0m'
URL_COLOR='\033[38;2;79;163;255m'  # Hellblau

# Funktion, die beim Abbruch oder Skriptende ausgeführt wird
cleanup() {
    printf "\n${YELLOW}[INFO] Abbruch erkannt, beende Docker und entferne Datenbank...${RESET}\n"
    docker-compose down --remove-orphans
    rm -f ./data/gcn.db*
    exit 0
}

# Trap für Strg+C (SIGINT) und andere Abbruchsignale
trap cleanup SIGINT SIGTERM

# Hauptoperationen
printf "\n${YELLOW}[INFO] Erstelle Dummy-Datenbankdatei...${RESET}\n"
dd if=/dev/zero of=./data/gcn.db bs=1K count=21543

printf "\n${YELLOW}[INFO] Starte Docker-Container...${RESET}\n"
docker-compose up --build -d

printf "\n${YELLOW}[INFO] Server läuft auf ${URL_COLOR}http://127.0.0.1:8080${RESET}\n"
printf "\n${YELLOW}[INFO] Docker-Logs werden angezeigt. Mit Strg+C kannst du abbrechen.${RESET}\n"

docker-compose logs -f

# Falls Logs normal enden, ebenfalls aufräumen
cleanup
