#!/bin/bash

# Funktion, die beim Abbruch oder Skriptende ausgeführt wird
cleanup() {
    echo -e "\n[INFO] Abbruch erkannt, beende Docker und entferne Datenbank..."
    docker-compose down --remove-orphans
    rm -f ./data/gcn.db*
    exit 0
}

# Trap für Strg+C (SIGINT) und andere Abbruchsignale
trap cleanup SIGINT SIGTERM

# Hauptoperationen
echo "[INFO] Erstelle Dummy-Datenbankdatei..."
dd if=/dev/zero of=./data/gcn.db bs=1K count=21543

echo "[INFO] Starte Docker-Container..."
docker-compose up --build -d

echo "[INFO] Docker-Logs werden angezeigt. Mit Strg+C kannst du abbrechen."
docker-compose logs -f

# Falls Logs normal enden, ebenfalls aufräumen
cleanup
