# 🛠️ Roadmap – Embedded Admin Frontend

## ✅ Aktuell umgesetzt
- Systemstatus (Load, Uptime, SD-Karte)
- Netzwerkstatus (Signal, VPN, Carrier)
- Containerstatus (Docker)
- Datenbankinfos (Größe, letzte Aktualisierung)
- Log-Viewer mit:
  - Level-Filter
  - Zeilenlimit
  - Farb-Toggle
  - Neueinträge via Dialog + Tastatursteuerung
- Auto-Refresh-Button (manuell/automatisch)
- Moderne Login-Seite mit Theme-Toggle
- Komponentisierte Card-Headers
- Mock-Backend mit Testdaten

---

## 🚀 Phase 1 – Anbindung & Authentifizierung
### Ziel: System sicher und echtzeitfähig mit dem Backend verbinden
- [ ] FastAPI-Anbindung für Systemdaten (`GET /api/...`)
- [ ] Authentifizierung (Session, Token)
- [ ] Weiterleitung auf Login bei ungültiger Session
- [ ] POST-Calls für Shutdown, Reboot, DB-Reset
- [ ] POST für neue Logeinträge

---

## ⚙️ Phase 2 – Systemdiagnose & Interaktivität
### Ziel: Mehr Kontrolle und Feedback über das System ermöglichen
- [ ] CPU-Auslastung (live)
- [ ] RAM/Swap-Anzeige
- [ ] Temperaturanzeige (optional)
- [ ] Netzwerkdurchsatz (RX/TX)
- [ ] VPN-Peer-Daten
- [ ] Containersteuerung (Start/Stop/Restart)
- [ ] Health-Status von Containern
- [ ] Live-Container-Logs
- [ ] Logs: Suche, Export (CSV/JSON), Auto-Refresh

---

## 🧩 Phase 3 – Konfiguration & Verwaltung
### Ziel: Admin-Funktionen für Dauerbetrieb und Fernwartung
- [ ] Zeitzone / Uhrzeit setzen
- [ ] Netzwerkkonfiguration (LAN/WLAN)
- [ ] Updateverwaltung
- [ ] Benutzerverwaltung (Rollen, Passwortänderung)
- [ ] Backup & Restore der Datenbank
- [ ] Export Systemstatus
- [ ] Log-Retention-Policy

---

## ✨ Phase 4 – Finishing Touches & Optimierung
### Ziel: UX/Design & Performance verbessern
- [ ] Responsive-Optimierung für kleine Displays
- [ ] Theme-Auswahl (Auto / Light / Dark)
- [ ] Offline-Anzeige & Retry bei API-Fehler
- [ ] E2E-Tests mit Playwright oder Cypress
- [ ] Umschaltbares `useMockData()` für Dev-Umgebungen
