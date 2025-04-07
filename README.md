# FastAPI Test

## PyCharm

1. Öffne “Run Configurations”
   1. Gehe zu Run → Edit Configurations.
   1. Falls keine Konfiguration existiert, klicke auf + (Add new configuration) und wähle Python. 
1. Ändere die Einstellungen
   1. Module: `uvicorn`
   2. Parameters: `app.main:app --reload`
   3. Python interpreter: Wähle den Interpreter deiner virtuellen Umgebung (venv).
1. Speichern und ausführen

## Terminal

Im Projektordner:

```zsh
source .venv/bin/activate
uvicorn app.main:app --reload
```

## Testing

Testdateien erzeugen

```zsh
dd if=/dev/zero of=./data/gcn.db bs=1K count=54321
```

Container Liste gekürzt

```zsh
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.RunningFor}}\t{{.Status}}\t{{.Names}}"
```

## Nuxt Projekt einrichten: `frontend/`

### 1. Abhängigkeiten installieren

```bash
npm install
```

### 2. Entwicklungsserver starten

```bash
npm run dev
```

Optional im Netzwerk erreichbar:

```bash
npm run dev -- --host
```

### 3. Node.js-Version prüfen (empfohlen: LTS)

```bash
node -v
```

### 4. (Optional) ShadCN-Komponenten initialisieren

```bash
npx shadcn-nuxt init
```
