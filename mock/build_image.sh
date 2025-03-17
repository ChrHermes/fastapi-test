#!/bin/bash

# Prüfe, ob eine .env-Datei existiert und lade die Variablen
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env-Datei nicht gefunden!"
    exit 1
fi

# Überprüfe, ob alle erforderlichen Variablen gesetzt sind
if [ -z "$USERNAME" ] || [ -z "$PAT" ] || [ -z "$REGISTRY" ] || [ -z "$REPO" ]; then
    echo "Mindestens eine erforderliche Umgebungsvariable fehlt. Bitte prüfe deine .env-Datei."
    exit 1
fi

# Konvertiere Username und Repository-Name in Kleinbuchstaben
USERNAME_LOWER=$(echo "$USERNAME" | tr '[:upper:]' '[:lower:]')
REPO_LOWER=$(echo "$REPO" | tr '[:upper:]' '[:lower:]')

# Überprüfe, ob ein Tag als Parameter übergeben wurde
if [ -z "$1" ]; then
    echo "Usage: $0 <tag>"
    exit 1
fi

TAG="$1"
IMAGE_TAG="$REGISTRY/$USERNAME_LOWER/$REPO_LOWER:$TAG"

# Anmeldung an der Registry
echo "Melde mich an der Registry $REGISTRY an..."
echo "$PAT" | docker login $REGISTRY -u "$USERNAME" --password-stdin
if [ $? -ne 0 ]; then
    echo "Docker login fehlgeschlagen!"
    exit 1
fi

# Baue das Image und tagge es
echo "Baue das Image mit Tag $IMAGE_TAG..."
docker build -t "$IMAGE_TAG" .

if [ $? -eq 0 ]; then
    echo "Image erfolgreich gebaut: $IMAGE_TAG"
else
    echo "Fehler beim Bauen des Images."
    exit 1
fi

# Pushe das Image in die Registry
echo "Pushe das Image $IMAGE_TAG..."
docker push "$IMAGE_TAG"

if [ $? -eq 0 ]; then
    echo "Image erfolgreich gepusht: $IMAGE_TAG"
else
    echo "Fehler beim Pushen des Images."
    exit 1
fi
