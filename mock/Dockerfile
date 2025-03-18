# Basis-Image
FROM alpine:latest

# Mehrere Labels zur Beschreibung des Images
LABEL Version="1.0.3-ghwe3m" \
      Description="Mock Docker Image mit zahlreichen Layern und zusätzlichen Labels" \
      Maintainer="dein_email@example.com" \
      BuildDate="2025-03-17" \
      Commit="abcdef1234567890" \
      Environment="Test" \
      OS="Alpine Linux" \
      License="MIT" \
      Vendor="YourCompany" \
      Architecture="x86_64" \
      Feature="Mehrere Layer und Labels"

# Layer 1: System aktualisieren und mehrere Utilities installieren
RUN apk update && apk add --no-cache curl wget bash zsh

# Layer 2: Erstellen des Arbeitsverzeichnisses
RUN mkdir -p /app

# Layer 3: Eine Dummy-Datei erzeugen
RUN echo "Dies ist eine Dummy-Datei." > /app/dummy.txt

# Layer 4: Zusätzlichen Inhalt an die Dummy-Datei anhängen
RUN echo "Weitere Inhalte werden hinzugefügt." >> /app/dummy.txt

# Layer 5: Zusätzlichen Ordner für Logs erstellen
RUN mkdir -p /app/logs

# Layer 6: Eine Log-Datei initialisieren
RUN echo "Log gestartet am $(date)" > /app/logs/log.txt

# Layer 7: Eine Konfigurationsdatei erstellen
RUN echo "config_value=42" > /app/config.ini

# Layer 8: Ein einfaches Shell-Skript erstellen
RUN echo "#!/bin/sh\n echo 'Custom Script läuft...'" > /app/run.sh && chmod +x /app/run.sh

# Layer 9: Eine Beispiel-Datei per wget herunterladen (Dummy-Download, URL muss erreichbar sein)
RUN wget -O /app/sample.txt https://www.example.com || echo "Download fehlgeschlagen, Dummy-Inhalt wird verwendet" && \
    echo "Dies ist ein Platzhalter für sample.txt" > /app/sample.txt

# Layer 10: Bereinigen des Paket-Cache
RUN rm -rf /var/cache/apk/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# Standardbefehl: Ausführen des Shell-Skripts
CMD ["sh", "run.sh"]
