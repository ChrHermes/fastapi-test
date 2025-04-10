# 📌 Funktions-Roadmap: Backend-API (FastAPI)

## ✅ Bereits implementierte Routen

| Bereich         | Methode | Route                          | Beschreibung                          |
|----------------|---------|---------------------------------|----------------------------------------|
| System          | POST    | `/system/shutdown`             | System herunterfahren                 |
| System          | POST    | `/system/reboot`               | System neustarten                     |
| Datenbank       | GET     | `/database/info`               | Metadaten zur SQLite-Datenbank        |
| Datenbank       | POST    | `/database/reset`              | Datenbankdatei löschen und neu starten |
| Docker          | GET     | `/docker/containers/`          | Laufende Container abrufen            |
| Docker          | GET     | `/docker/registry/images`      | Verfügbare Images aus Registry        |
| Docker          | GET     | `/docker/updates`              | Versionsvergleich Registry vs. Container |
| Docker          | POST    | `/docker/update`               | `docker-compose pull` ausführen       |
| Docker          | POST    | `/docker/restart`              | `docker-compose restart` ausführen    |

---

## 🧩 Geplante / sinnvolle Erweiterungen

### 🔧 Systemstatus & Umgebung

| Methode | Route               | Beschreibung                                  |
|---------|---------------------|-----------------------------------------------|
| GET     | `/system/info`      | Hostname, Zeit, Uptime, LoadAvg               |
| GET     | `/system/storage`   | Speicherbelegung (SD, Mountpoints)            |
| GET     | `/system/time`      | Systemzeit, Zeitzone                          |
| GET     | `/system/health`    | Gesamtstatus / Ampelsystem                    |

---

### 🌐 Netzwerkinformationen

| Methode | Route                 | Beschreibung                                |
|---------|-----------------------|---------------------------------------------|
| GET     | `/network/info`       | IPs, Gateway, DNS, Interfaces               |
| GET     | `/network/modem`      | Signalstärke, Typ (LTE/EDGE), IP, Carrier   |
| GET     | `/network/netbird`    | Status, Peer-IP, Latenz, Version            |
| POST    | `/network/reconnect`  | (optional) Verbindungen neu aufbauen        |

---

### 📜 Protokolle / Logs

| Methode | Route                       | Beschreibung                                   |
|---------|-----------------------------|------------------------------------------------|
| GET     | `/logs`                     | Logeinträge (filterbar per Level, Limit)       |
| POST    | `/logs`                     | Benutzerdefinierter Logeintrag hinzufügen      |
| GET     | `/logs/container/{id}`      | Logs eines spezifischen Containers abrufen     |

---

### 🛡️ Authentifizierung

| Methode | Route              | Beschreibung                        |
|---------|--------------------|-------------------------------------|
| POST    | `/auth/login`      | Benutzeranmeldung                   |
| POST    | `/auth/validate`   | Token-Validierung                   |
| POST    | `/auth/logout`     | (optional) Logout                   |

---

### ⚙️ Einstellungen (zukünftig)

| Methode | Route         | Beschreibung                               |
|---------|---------------|--------------------------------------------|
| GET     | `/settings`   | System-/App-Einstellungen abrufen          |
| POST    | `/settings`   | Einstellungen aktualisieren/persistieren  |

---

### 🧪 Diagnose / Datei-Zugriff

| Methode | Route                        | Beschreibung                             |
|---------|------------------------------|------------------------------------------|
| GET     | `/files/list?path=...`       | Auflistung von Dateien in einem Verzeichnis |
| GET     | `/files/download?path=...`   | Datei herunterladen                      |

---

## 📘 Hinweise

- Alle Routen sollten idealerweise Authentifizierung (z. B. JWT) voraussetzen.
- Bei containerbezogenen Aktionen ggf. Fehlerbehandlung für `DockerClientNotAvailable`, `ContainerNotFound`, etc.
- Alle Rückgaben sollten konsistent strukturiert werden (z. B. `{ "status": "ok", "data": ... }`)

---

✅ Diese Roadmap kann als Grundlage für die API-Dokumentation und zukünftige Features dienen.
