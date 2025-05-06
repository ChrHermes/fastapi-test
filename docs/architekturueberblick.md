# Architekturüberblick – GCA Stand 6. Mai 2025, 18:00h

## Allgemeines

- **Projektziel:** Kombination aus leichtgewichtiger Admin-UI und Systemstatus-Anzeige für Embedded-Controller (Docker + BusyBox)
- **Zielsystem:** Linux ARMv7 mit privilegiertem Container
- **Hostzugriff:** per `/host` gemountetes Root-Verzeichnis für Systemdaten
- **Containerarchitektur:** All-in-One Image mit FastAPI (Backend) + statischem Nuxt (Frontend)

---

## Backend (FastAPI)

- **Framework:** FastAPI
- **Struktur:** Aufteilung in `routes/`, `services/`, `schemas/`, `utils/`
- **Build:** `.pyc`-Kompilierung im Container zur Reduzierung und Obfuskation
- **Security:**
  - Cookie-basierte Authentifizierung (kein JWT)
  - `require_auth`-Dependency schützt API-Routen
  - `MOCK_MODE` in Routen trennbar
- **Systemdatenquellen:**
  - `/host/proc/` für `uptime`, `loadavg`, `meminfo`, `stat`, `net/dev`
  - `subprocess` für `df`, `uptime`, `netbird status`
- **Nützliche Services:**
  - `system_service.py` für systemnahe Informationen
  - `log_service.py`, `docker_service.py` u. a.

---

## Frontend (Nuxt 3)

- **Rendering-Modus:** statisch gerendert (SSG) für Integration mit FastAPI
- **Komponenten:**
  - Statuskarten (`SystemInfoCard`, `DiskUsageCard`, `MemoryUsageCard`, `ModemInfo`, etc.)
  - `InfoPopover`, `ColorModeToggle`, `CardSectionHeader`
- **Design/UX:**
  - TailwindCSS mit `@shadcn/ui`
  - Doughnut-Charts (Chart.js) für RAM/Disk-Visualisierung
  - Responsive Grid (`grid-cols-1 md:grid-cols-2`)
- **Auth:**
  - `useAuth.ts` mit Cookie-basiertem Login
  - `auth.ts` Middleware (global im `default.vue` Layout)

---

## Dev/Build

- **Build-Skript:** `build.sh`
  - `--build-fe`, `--arm`, `--export`, `--clean`, `--clean-only`
  - Plattformwahl + Metriken (Image-Größe, Layeranzahl)
- **Dev-Modus:**
  - `dev.sh` für lokalen FastAPI Start mit `.venv`
  - optionales separates Nuxt-Frontend über `npm run dev`
- **Größe:** aktuelles Image ~120 MB bei `.pyc`-Build

---

## Zabbix Agent

- **Einsatz:** Monitoring via Docker-Container
- **Basis:** `zabbix-agent2:alpine-7.2-latest`, privilegiert
- **Konfig:** lokale `zabbix_agent2.conf` + Plugin-Ordner (z. B. Docker)
- **Hostzugriff:** `/:/host:ro`
- **Statusprüfungen via:** Zabbix-Keys, Docker, NetBird, Filesystem etc.

---

## Erweiterungsideen

- 🧠 Drag & Drop / Collapsible Cards (Vue Draggable?)
- 📊 Charts für Langzeitwerte (z. B. Load, Speichertrend)
- 🔧 Mehr Detailseiten (Docker-Logs, Containersteuerung)
- 🔐 Session-Erhalt beim Refresh (Nuxt `useCookie` statt nur `useState`)
- 🐧 Integration von Systemtools wie `smartctl`, `iostat`, etc.

---