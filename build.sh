#!/bin/bash
set -e

# ----------- Farben -----------
RESET='\033[0m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[1;34m'

# ----------- Logging Funktionen -----------
info()    { printf "\n${YELLOW}%s${RESET}\n" "$1"; }
error()   { printf "${RED}%s${RESET}\n" "$1"; }
success() { printf "\n${GREEN}%s${RESET}\n" "$1"; }
detail()  { printf "${BLUE}%s${RESET}\n" "$1"; }

# ----------- Konfiguration -----------
IMAGE_NAME="gc-admin"
IMAGE_VERSION="latest"
IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"

DOCKERFILE="Dockerfile"
EXPORT_DIR="./prod"
EXPORT_IMAGE_NAME="gc-admin.tar"
EXPORT_ARCHIVE_NAME="gc-admin.tar.gz"
PLATFORM="linux/amd64"

CLEAN_MODE=false

# ----------- Parameter parsen -----------
EXPORT_ENABLED=false
BUILD_FE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --arm)
            PLATFORM="linux/arm/v7"
            IMAGE_VERSION="armv7"
            IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"
            shift
            ;;
        --tag)
            IMAGE_VERSION="$2"
            IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"
            shift 2
            ;;
        --export)
            EXPORT_ENABLED=true
            shift
            ;;
        --build-fe)
            BUILD_FE=true
            shift
            ;;
        --clean)
            --clean)
            CLEAN_MODE=true
            shift
            ;;
        --help)
            echo "Nutzung: $0 [Optionen]"
            echo ""
            echo "  --build-fe       Frontend (Nuxt) vor dem Docker-Build erstellen"
            echo "  --arm            Baue Image für ARMv7 (linux/arm/v7)"
            echo "  --tag VERSION    Docker-Tag überschreiben (z. B. dev, test)"
            echo "  --export         Image als .tar + .tar.gz exportieren"
            echo "  --help           Diese Hilfe anzeigen"
            exit 0
            ;;
        *)
            error "Unbekannte Option: $1"
            exit 1
            ;;
    esac
done

# ----------- Optionales Frontend-Build -----------
if [ "$BUILD_FE" = true ]; then
    info "---------- 🌐 Baue Frontend ----------"
    cd frontend
    npm install
    npm run build
    cd ..
    mkdir -p dist/frontend
    cp -r frontend/.output/public/* dist/frontend/
    success "✅ Frontend-Build abgeschlossen → dist/frontend/"
fi

# ----------- Build starten -----------
info "---------- 🚀 Baue Docker-Image ----------"
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

# ----------- Image-Details -----------
info "---------- 📊 Image-Statistiken ----------"
size_bytes=$(docker image inspect "$IMAGE_TAG" --format='{{.Size}}')
size_mb=$(echo "scale=2; $size_bytes / 1024 / 1024" | bc)
layer_count=$(docker history --no-trunc "$IMAGE_TAG" | grep -v '<missing>' | wc -l)

detail "- Größe: $size_bytes Bytes ($size_mb MB)"
detail "- Layer: $layer_count"

# ----------- Export falls aktiviert -----------
if [ "$EXPORT_ENABLED" = true ]; then
    info "---------- 📦 Exportiere Image ----------"
    mkdir -p "$EXPORT_DIR"
    docker save "$IMAGE_TAG" -o "$EXPORT_DIR/$EXPORT_IMAGE_NAME"

    info "---------- 📦 Erstelle Archiv ----------"
    tar czvf "$EXPORT_ARCHIVE_NAME" -C "$EXPORT_DIR" .

    success "✅ Exportiert nach: $EXPORT_IMAGE_NAME & $EXPORT_ARCHIVE_NAME"
fi

# ----------- Clean-Modus -----------
if [ "$CLEAN_MODE" = true ]; then
    info "---------- 🧹 Bereinige Build-Artefakte ----------"
    rm -rf dist/frontend
    rm -rf prod
    rm -rf frontend/.output
    success "✅ Alles bereinigt."
    exit 0
fi