#!/bin/bash
set -e

# ----------- Konfiguration -----------
IMAGE_NAME="gc-admin"
IMAGE_VERSION="latest"
IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"

DOCKERFILE="Dockerfile"
EXPORT_DIR="./prod"
EXPORT_IMAGE_NAME="gc-admin.tar"
EXPORT_ARCHIVE_NAME="gc-admin.tar.gz"
PLATFORM="linux/amd64"

# ----------- Farben -----------
RESET='\033[0m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[1;34m'

# ----------- Logging Funktionen -----------
info() {
    printf "${YELLOW}%s${RESET}\n\n" "$1"
}

error() {
    printf "${RED}%s${RESET}\n" "$1"
}

success() {
    printf "${GREEN}%s${RESET}\n" "$1"
}

detail() {
    printf "${BLUE}%s${RESET}\n" "$1"
}

show_help() {
    echo "Nutzung: $0 [OPTIONEN]"
    echo ""
    echo "Optionen:"
    echo "  --arm           Baue für ARMv7 (plattform: linux/arm/v7)"
    echo "  --tag NAME      Setzt den Docker-Image-Tag (default: $IMAGE_TAG)"
    echo "  --export        Exportiert das Image als .tar + Archiv"
    echo "  --help          Diese Hilfe anzeigen"
    exit 0
}

# ----------- Parameter parsen -----------
EXPORT_ENABLED=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --arm)
            PLATFORM="linux/arm/v7"
            IMAGE_VERSION="armv7"
            IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"
            shift
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --export)
            EXPORT_ENABLED=true
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            error "Unbekannte Option: $1"
            show_help
            ;;
    esac
done

# ----------- Build starten -----------
info "--- 🚀 Baue Docker-Image ---"
detail " - Name:       $IMAGE_NAME"
detail " - Version:    $IMAGE_VERSION"
detail " - Plattform:  $PLATFORM"
detail " - Dockerfile: $DOCKERFILE"
detail " - Tag:        $IMAGE_TAG"
echo ""

docker buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" --load -f "$DOCKERFILE" . || {
    error "❌ Build fehlgeschlagen"
    exit 1
}
success "✅ Build erfolgreich abgeschlossen"

# ----------- Details anzeigen -----------
info "--- 📊 Image-Statistiken ---"

# Größe in Bytes + MB berechnen
size_bytes=$(docker image inspect "$IMAGE_TAG" --format='{{.Size}}')
size_mb=$(echo "scale=2; $size_bytes / 1024 / 1024" | bc)
# Layer-Anzahl ermitteln
layer_count=$(docker history --no-trunc "$IMAGE_TAG" | grep -v '<missing>' | wc -l)

detail " - Größe: $size_bytes Bytes ($size_mb MB)"
detail " - Layer: $layer_count"

# ----------- Export falls aktiviert -----------
if [ "$EXPORT_ENABLED" = true ]; then
    info "--- 📦 Exportiere Image ---"
    mkdir -p "$EXPORT_DIR"
    docker save "$IMAGE_TAG" -o "$EXPORT_DIR/$EXPORT_IMAGE_NAME"

    info "--- 📦 Erstelle Archiv ---"
    tar czvf "$EXPORT_ARCHIVE_NAME" -C "$EXPORT_DIR" .

    success "✅ Image exportiert nach $EXPORT_DIR/$EXPORT_IMAGE_NAME und $EXPORT_ARCHIVE_NAME"
fi
