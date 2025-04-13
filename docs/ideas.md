# 💡 GC-Admin Roadmap & Ideen

## 🔌 Funktionale Erweiterungen

### Zabbix-Agent Integration
- Anbindung an lokalen Zabbix-Agent (Docker-Host)
- Anzeige von:
  - CPU-, RAM-, Netzwerk- und Filesystem-Auslastung
  - Prozesse und Systemzustand
  - Docker-spezifische Zabbix-Werte
- Backend-Service: `zabbix_service.py`
- Später optional als Plugin-Architektur

---

### Speicheranzeige (Modular)
- Unterstützung für mehrere Partitionen/Mounts:
  - z. B. `/`, `/data`, `/mnt/sdcard`, Netzlaufwerke
- Anzeige von:
  - Nutzung in %
  - Freier Speicher
- Quellen: `df`, `mount`, API oder `/proc/mounts`
- Konfiguration über `.env`, WebUI oder autodiscovery

---

### Health-Stats als Komponenten
- Mini-Cards mit Statusanzeigen:
  - Load Average
  - RAM-Nutzung
  - SD-Karten-Auslastung
  - Docker-Status
- Farbliche Bewertung (Ampel)
- Tooltips mit InfoPopover
- Optional autorefresh einzeln aktivierbar

---

## 🧩 UX / Interface

### Movable & Collapsible Cards
- Drag'n'Drop via `vue-draggable-next` oder `vue-grid-layout`
- Collapse-Button pro Card
- Zustand speicherbar (localStorage / API / Userprefs)

---

### Konfigurierbares Dashboard
- Umschaltbare Sektionen (Toggles, Tabs oder Accordion)
- Einblendbare Cards (z. B. "Erweiterte Systeminfos")
- Rechtebasierte Anzeige: Admin vs. Viewer

---

### Wartungsmodus
- Globales Flag im Backend (z. B. über ENV)
- Anzeige eines Banners in der UI
- Optionale Deaktivierung kritischer Aktionen

---

## 🔒 Sicherheit & Erweiterbarkeit

- **JWT-basierte Auth** (optional zusätzlich zu Session)
- API-Key Support für externe Tools
- Logging: Aktionen der Nutzer (Login, Reset, etc.)
- Erweiterung durch **modulare Plugins** im Backend (admin tools)

---

## ✅ Nächste Umsetzungsschritte

- [ ] Collapse für alle Cards vereinheitlichen
- [ ] Speicher-Mounts ermitteln und anzeigen
- [ ] Health-Komponenten extrahieren
- [ ] Docker-Status zur Health-Card hinzufügen
- [ ] Vorbereitung Plugin-Loader (z. B. health_plugins)
