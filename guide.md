# GCN Docker Management Tool

## Anforderungen an das Projekt

### Allgemeine Architektur

- [x] Der Management-Service läuft als eigenständiger Container in einer Docker-Compose Umgebung.
- [ ] Er soll unabhängig von anderen Containern sein, aber bei Bedarf in einen bestehenden nginx integriert werden.
- [ ] Muss über HTTPS unter `/management` erreichbar sein.

### Funktionen des Management-Service

- [x] Backend-Container stoppen und Datenbank zurücksetzen:
  - [x] Löscht die Dateien `/media/sd/data/gcn.db` sowie zugehörige Cache-Dateien (`gcn.db-wal`, `gcn.db-journal`).
- [x] System sicher herunterfahren.
- [x] Logging:
  - [x] Aktionen werden in einem historischen Log gespeichert und für den Nutzer sichtbar gemacht.
  - [x] Nutzer können individuelle Nachrichten ins Log schreiben (z. B. Hinweise für Entwickler oder Vertrieb).
- [x] Kritische Aktionen mit Bestätigung:
  - [x] Bei sensiblen Aktionen erscheint ein Modal, in dem der Nutzer einen vorgegebenen Bestätigungstext eingeben muss (ähnlich wie bei GitLab beim Löschen eines Repos).

### Benutzerverwaltung & Sicherheit

- [x] Authentifizierung erforderlich, bevor ein Nutzer das Dashboard betreten kann.
- [x] Benutzername & Passwort dürfen nicht im Code stehen:
  - [x] Stattdessen werden sie über eine .env Datei in Kombination mit docker-compose geladen.
- [x] Sicherheit & Fehlerhandling:
  - [x] Container muss auch ohne direkten Zugriff auf die Mounts starten können (z. B. für Entwicklung).
  - [x] Falls kein Zugriff auf Docker möglich ist, startet der Service trotzdem und zeigt den Status an.

## Vorschläge für Verbesserungen

- **Bessere UI/UX für das Management-Dashboard**
  - [x] Nutzung von JavaScript (z. B. Vue.js oder Alpine.js) für eine dynamischere Oberfläche.
  - [ ] Automatische Aktualisierung der Logs ohne Seitenreload.
  - [ ] Verbesserung des Modal-Dialogs für kritische Aktionen (farbliche Hervorhebungen, bessere UX).
- **Fehlermanagement erweitern**
  - [ ] Detaillierte Fehlermeldungen mit Vorschlägen zur Behebung.
  - [x] Logging der Fehler in einer separaten Datei oder einem externen Logging-Service.
- **Rechteverwaltung**
  - [ ] Einführung von Rollen (z. B. Admin, Vertrieb, Entwickler), um den Zugriff auf Funktionen zu beschränken.
  - [ ] Einbindung eines OAuth2- oder
  - [ ] LDAP-Authentifizierungssystems für größere Umgebungen.
- **Automatisierte Backups der Datenbank**
  - [x] Möglichkeit, vor einem Reset automatisch ein Backup der gcn.db zu erstellen.
  - [ ] Download-Funktion für manuelle Sicherungen.
- **Mehr Kontrolle über Docker-Container**
  - [ ] Start/Stop anderer Container direkt aus der Weboberfläche.
  - [ ] Anzeige der aktuellen CPU- [ ] und Speicherauslastung der Container.
