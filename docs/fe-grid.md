### Grid-Layout (Container)

```html
<div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 auto-rows-[minmax(6rem,auto)]">
  <!-- Jede Komponente wird hier eingefügt -->
</div>
```

---

### Komponenten (Beispiele)

```vue
<Card class="col-span-1 row-span-1">
  <CardHeader>
    <CardTitle>Hostname</CardTitle>
  </CardHeader>
  <CardContent>
    <HostnameDisplay :hostname="system.hostname" />
  </CardContent>
</Card>

<Card class="col-span-2 row-span-2">
  <CardHeader>
    <CardTitle>Speicherplatz</CardTitle>
  </CardHeader>
  <CardContent>
    <DiskUsageList :disks="system.disk" />
  </CardContent>
</Card>
```

---

### Grid-Konfiguration der Komponenten

| Komponente         | Spalten | `col-span`     | Zeilen | `row-span`     | Begründung                                                        |
|--------------------|---------|----------------|--------|----------------|-------------------------------------------------------------------|
| Hostname + Uhrzeit | 1       | `col-span-1`   | 1      | `row-span-1`   | Wenig Inhalt, kurze Textanzeige                                   |
| Uptime             | 1       | `col-span-1`   | 1      | `row-span-1`   | Kompakt, einfache Darstellung                                     |
| Load Average       | 2       | `col-span-2`   | 1      | `row-span-1`   | Drei Balken nebeneinander benötigen etwas mehr Platz              |
| RAM Usage (Chart)  | 1       | `col-span-1`   | 2      | `row-span-2`   | Vertikale Darstellung, Platz für Beschriftungen und Diagramm      |
| Disk Usage         | 2       | `col-span-2`   | 2      | `row-span-2`   | Mehrere Disks mit Balken, ggf. Scrollbar notwendig                |
| Network Status     | 2       | `col-span-2`   | 2      | `row-span-2`   | Modemstatus, VPN-Details, Icons – benötigt Raum                   |
| Health Ampel       | 1       | `col-span-1`   | 1      | `row-span-1`   | Kleine kompakte Ampel, optisch hervorgehoben aber platzsparend    |
