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
warn()    { printf "${YELLOW}%s${RESET}\n" "$1"; }

# ----------- Funktionen -----------
clean_junk_files() {
    info "---------- 🧽 Entferne unnötige Systemdateien ----------"

    # Entfernt typische macOS & Windows & Editor-Artefakte
    find . \( \
        -name ".DS_Store" \
        -o -name "Thumbs.db" \
        -o -name "desktop.ini" \
        -o -name "._*" \
        -o -name ".AppleDouble" \
        -o -name ".LSOverride" \
        -o -name "Icon\r" \
        -o -name "*~" \
        -o -name "*.swp" \
        -o -name "*.tmp" \
    \) -type f -delete

    success "✅ Junk-Dateien entfernt"
}

# ----------- Konfiguration -----------
IMAGE_NAME="gc-admin"
IMAGE_VERSION="latest"
IMAGE_TAG="${IMAGE_NAME}:${IMAGE_VERSION}"

DOCKERFILE="Dockerfile"
EXPORT_DIR="./prod"
PLATFORM="linux/amd64"

CLEAN_MODE=false
CLEAN_ONLY=false

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
            CLEAN_MODE=true
            shift
            ;;
        --clean-only)
            CLEAN_ONLY=true
            shift
            ;;
        --help)
            echo -e "${YELLOW}Nutzung:${RESET} $0 [Optionen]"
            echo ""
            echo -e "${BLUE}Build-Optionen:${RESET}"
            echo "  --build-fe        Frontend (Nuxt) vor dem Docker-Build erstellen"
            echo "  --arm             Baue Image für ARMv7 (plattform: linux/arm/v7)"
            echo "  --tag VERSION     Docker-Tag überschreiben (z. B. dev, test)"
            echo "  --export          Exportiere Image als .tar + .tar.gz"

            echo ""
            echo -e "${BLUE}Wartung:${RESET}"
            echo "  --clean           Entfernt dist/frontend, prod/ und .output"
            echo "  --clean-only      Nur aufräumen, kein Build"

            echo ""
            echo -e "${BLUE}Sonstiges:${RESET}"
            echo "  --help            Diese Hilfe anzeigen"

            echo ""
            echo -e "${YELLOW}Systeminfos:${RESET}"
            echo -n "  Architektur:     "; uname -m
            echo -n "  Docker Version:  "; docker --version | cut -d ' ' -f1-3
            echo -n "  Docker Buildx:   "; docker buildx version | head -n1 || echo "❌ nicht verfügbar"
            echo -n "  BuildKit aktiv:  "; echo ${DOCKER_BUILDKIT:-"nicht gesetzt"}

            exit 0
            ;;
        *)
            error "Unbekannte Option: $1"
            exit 1
            ;;
    esac
done

# ----------- Clean-Modus -----------
if [ "$CLEAN_ONLY" = true ]; then
    info "---------- 🧹 Bereinige Build-Artefakte ----------"
    rm -rf dist/frontend
    rm -rf prod
    rm -rf frontend/.output
    success "✅ Alles bereinigt."

    # Skript beenden
    exit 0
fi

START_TIME=$(date +%s)

# ----------- Unerwünschte Dateien löschen (z. B. .DS_Store) -----------
clean_junk_files

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

    # 💡 Größe anzeigen
    fe_size_kb=$(du -sk dist/frontend | cut -f1)
    fe_size_mb=$(awk "BEGIN { printf \"%.2f\", $fe_size_kb / 1024 }")
    detail " - Größe Frontend-Output: ${fe_size_mb} MB"
fi

# ----------- FE-Ordner-Prüfung -----------
if [ ! -d "dist/frontend" ]; then
    error "❌ dist/frontend nicht gefunden. Bitte vorher mit --build-fe erstellen!"
    exit 1
fi

# ----------- Build starten -----------
info "---------- 🚀 Baue Docker-Image ----------"
detail " - Name:       $IMAGE_NAME"
detail " - Version:    $IMAGE_VERSION"
detail " - Plattform:  $PLATFORM"
detail " - Dockerfile: $DOCKERFILE"
detail " - Tag:        $IMAGE_TAG"
echo ""

if [[ "$PLATFORM" == "linux/arm/v7" ]]; then
    docker buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" --load -f "$DOCKERFILE" . || {
        error "❌ Build fehlgeschlagen (buildx)"
        exit 1
    }
else
    docker build -t "$IMAGE_TAG" -f "$DOCKERFILE" . || {
        error "❌ Build fehlgeschlagen (docker)"
        exit 1
    }
fi

success "✅ Build erfolgreich abgeschlossen"

# ----------- Image-Details -----------
info "---------- 📊 Image-Statistiken ----------"

if docker image inspect "$IMAGE_TAG" &>/dev/null; then
    size_bytes=$(docker image inspect "$IMAGE_TAG" --format='{{.Size}}')
    size_mb=$(awk "BEGIN { printf \"%.2f\", $size_bytes / 1024 / 1024 }")
    layer_count=$(docker history --no-trunc "$IMAGE_TAG" | grep -v '<missing>' | wc -l)

    detail "- Größe: ${size_mb} MB"
    detail "- Layer: $layer_count"
else
    warn "⚠️  Image $IMAGE_TAG nicht lokal vorhanden (vermutlich ARM + buildx)"
fi

# ----------- Export falls aktiviert -----------
if [ "$EXPORT_ENABLED" = true ]; then
    EXPORT_IMAGE_NAME="gc-admin.$IMAGE_VERSION.tar"
    EXPORT_ARCHIVE_NAME="gc-admin.$IMAGE_VERSION.tar.gz"

    info "---------- 📦 Exportiere Image ----------"
    mkdir -pv "$EXPORT_DIR"
    docker save "$IMAGE_TAG" -o "$EXPORT_DIR/$EXPORT_IMAGE_NAME"

    info "---------- 📦 Erstelle Archiv ----------"
    tar czvf "$EXPORT_DIR/$EXPORT_ARCHIVE_NAME" "$EXPORT_DIR/$EXPORT_IMAGE_NAME"

    # ----------- Größen berechnen mit Nachkommastellen -----------
    tar_size_kb=$(du -k "$EXPORT_DIR/$EXPORT_IMAGE_NAME" | cut -f1)
    tar_size_mb=$(awk "BEGIN { printf \"%.2f\", $tar_size_kb / 1024 }")

    archive_size_kb=$(du -k "$EXPORT_DIR/$EXPORT_ARCHIVE_NAME" | cut -f1)
    archive_size_mb=$(awk "BEGIN { printf \"%.2f\", $archive_size_kb / 1024 }")

    success "✅ Export abgeschlossen:"
    detail " - Image-Archiv (.tar):     ${tar_size_mb} MB"
    detail " - Gesamtarchiv (.tar.gz):  ${archive_size_mb} MB"
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

# ----------- Zeitmessung -----------
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

info "---------- ⏱️ Gesamtzeit ----------"
detail " - Dauer: ${MINUTES}m ${SECONDS}s"
