export const mockSystem = {
    hostname: 'Vertriebsbox22',
    time: '2025-04-06 14:22:10',
    uptime: '3 Tage, 4 Stunden',
    load: {
        '1m': 2.97,
        '5m': 1.55,
        '15m': 0.96,
    },
    disk: [
        {
            label: 'Intern',
            used: '3.22 GB',
            total: '4 GB',
            percent: 80.5,
        },
        {
            label: 'SD-Karte',
            used: '3.7 GB',
            total: '8 GB',
            percent: 46.25,
            // used: '6.7 GB',
            // total: '8 GB',
            // percent: 83.75,
        },
    ],
}

export const mockNetwork = {
    modem: {
        signal: -59,
        // signal: -75,
        // signal: -99,
        // network: 'EDGE',
        // network: 'GPRS',
        network: 'LTE',
        carrier: 'Telekom',
        ip: '10.143.8.21',
    },
    netbird: {
        status: 'Verbunden',
        peer_ip: '100.72.42.12/21',
        latency: '48.9754ms',
        version: '0.35.2',
    },
}

export const mockDatabase = {
    size: 120.03,
    created: '2024-08-22 10:15:00',
    updated: '2025-04-06 13:57:23',
}

export const mockContainers = [
    {
        id: 'ab1234',
        name: 'backend',
        image: 'https://company.intern.gitlab.com:8480/example-group-1/application-backend:latest',
        version: '1.1.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        id: 'bc2345',
        name: 'frontend',
        image: 'frontend:latest',
        version: '1.0.18',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        id: 'cd3456',
        name: 'fieldcom',
        image: 'fieldcom:latest',
        version: '1.0.12',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        id: 'de4567',
        name: 'gateway',
        image: 'gateway:latest',
        version: '1.1.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        id: 'ef5678',
        name: 'cellular',
        image: 'cellular:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        id: 'fg6789',
        name: 'base',
        image: 'base:latest',
        version: '1.0.8',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
]

export const mockLogs = [
    {
        timestamp: '2025-04-07 10:00:12',
        level: 'INFO',
        message: 'System gestartet',
    },
    {
        timestamp: '2025-04-07 10:01:00',
        level: 'USER',
        message: 'Neustart ausgelöst',
    },
    {
        timestamp: '2025-04-07 10:02:34',
        level: 'ERROR',
        message: 'Fehler beim Modem',
    },
    { timestamp: '2025-04-07 10:03:15', level: 'DEBUG', message: 'Ping 48ms' },
    {
        timestamp: '2025-04-07 10:04:05',
        level: 'INFO',
        message: 'Netzwerkverbindung aufgebaut',
    },
    {
        timestamp: '2025-04-07 10:04:45',
        level: 'USER',
        message: 'Updateprüfung manuell gestartet',
    },
    {
        timestamp: '2025-04-07 10:05:10',
        level: 'INFO',
        message: 'Docker-Container gestartet: backend',
    },
    {
        timestamp: '2025-04-07 10:06:00',
        level: 'ERROR',
        message: 'Verbindungsfehler zum MQTT-Broker',
    },
    {
        timestamp: '2025-04-07 10:06:30',
        level: 'DEBUG',
        message: 'Signalstärke: -72 dBm',
    },
    {
        timestamp: '2025-04-07 10:07:22',
        level: 'INFO',
        message: 'Uhrzeit synchronisiert',
    },
    {
        timestamp: '2025-04-07 10:08:00',
        level: 'USER',
        message: 'Log-Level auf DEBUG gesetzt',
    },
    {
        timestamp: '2025-04-07 10:08:42',
        level: 'DEBUG',
        message: 'Container logs eingelesen',
    },
    {
        timestamp: '2025-04-07 10:09:12',
        level: 'INFO',
        message: 'VPN-Verbindung aktiv',
    },
    {
        timestamp: '2025-04-07 10:09:58',
        level: 'DEBUG',
        message: 'Antwortzeit: 32ms',
    },
    {
        timestamp: '2025-04-07 10:10:05',
        level: 'USER',
        message: 'Diagnosebericht exportiert',
    },
    {
        timestamp: '2025-04-07 10:11:03',
        level: 'ERROR',
        message: 'Speicherzugriffsfehler bei Modul XY',
    },
    {
        timestamp: '2025-04-07 10:11:59',
        level: 'INFO',
        message: 'Konfiguration gespeichert',
    },
    {
        timestamp: '2025-04-07 10:12:34',
        level: 'DEBUG',
        message: 'Interface eth0 aktiv',
    },
    {
        timestamp: '2025-04-07 10:13:13',
        level: 'INFO',
        message: 'Watchdog zurückgesetzt',
    },
    {
        timestamp: '2025-04-07 10:14:00',
        level: 'USER',
        message: 'Systemupdate durchgeführt',
    },
    {
        timestamp: '2025-04-07 10:14:48',
        level: 'INFO',
        message: 'Neustart erforderlich',
    },
    {
        timestamp: '2025-04-07 10:15:22',
        level: 'ERROR',
        message: 'Fehler beim Mounten der SD-Karte',
    },
    {
        timestamp: '2025-04-07 10:16:05',
        level: 'DEBUG',
        message: 'Aktuelle Temperatur: 48°C',
    },
    {
        timestamp: '2025-04-07 10:16:42',
        level: 'INFO',
        message: 'NTP-Server antwortet',
    },
    {
        timestamp: '2025-04-07 10:17:20',
        level: 'USER',
        message: 'Debug-Modus aktiviert',
    },
    {
        timestamp: '2025-04-07 10:18:05',
        level: 'INFO',
        message: 'Konfigurationsprüfung abgeschlossen',
    },
    {
        timestamp: '2025-04-07 10:18:55',
        level: 'ERROR',
        message: 'Konnektivitätsverlust festgestellt',
    },
    {
        timestamp: '2025-04-07 10:19:34',
        level: 'DEBUG',
        message: 'Netzwerküberwachung aktiv',
    },
    {
        timestamp: '2025-04-07 10:20:22',
        level: 'INFO',
        message: 'Firmware-Version 1.0.5 aktiv',
    },
    {
        timestamp: '2025-04-07 10:21:00',
        level: 'USER',
        message: 'Gerätekennung aktualisiert',
    },
    {
        timestamp: '2025-04-07 10:21:45',
        level: 'DEBUG',
        message: 'Datenbankgröße: 120 MB',
    },
    {
        timestamp: '2025-04-07 10:22:33',
        level: 'INFO',
        message: 'Systemstatus OK',
    },
    {
        timestamp: '2025-04-07 10:23:17',
        level: 'ERROR',
        message: 'Systemzeit weicht ab',
    },
    {
        timestamp: '2025-04-07 10:24:02',
        level: 'INFO',
        message: 'Netzwerkprofil geladen',
    },
    {
        timestamp: '2025-04-07 10:25:12',
        level: 'DEBUG',
        message: 'Ping zur Cloud: 45ms',
    },
    {
        timestamp: '2025-04-07 10:26:08',
        level: 'INFO',
        message: 'Speicherplatz geprüft',
    },
    {
        timestamp: '2025-04-07 10:27:00',
        level: 'USER',
        message: 'Automatischer Reboot geplant',
    },
    {
        timestamp: '2025-04-07 10:28:00',
        level: 'DEBUG',
        message: 'Watchdog aktiv',
    },
    {
        timestamp: '2025-04-07 10:28:45',
        level: 'ERROR',
        message: 'Dateizugriffsfehler in /var/log',
    },
    {
        timestamp: '2025-04-07 10:29:30',
        level: 'INFO',
        message: 'Übertragungsrate stabil',
    },
    {
        timestamp: '2025-04-07 10:30:25',
        level: 'DEBUG',
        message: 'Load average: 0.92 / 1.03 / 1.22',
    },
    {
        timestamp: '2025-04-07 10:31:00',
        level: 'USER',
        message: 'Verbindung manuell getrennt',
    },
    {
        timestamp: '2025-04-07 10:31:59',
        level: 'INFO',
        message: 'Neustart abgeschlossen',
    },
    {
        timestamp: '2025-04-07 10:32:40',
        level: 'ERROR',
        message: 'Systemtemperatur kritisch',
    },
    {
        timestamp: '2025-04-07 10:33:25',
        level: 'DEBUG',
        message: 'Modemstatus geprüft',
    },
    {
        timestamp: '2025-04-07 10:34:18',
        level: 'INFO',
        message: 'Update erfolgreich installiert',
    },
    {
        timestamp: '2025-04-07 10:35:10',
        level: 'USER',
        message: 'Datenexport gestartet',
    },
    {
        timestamp: '2025-04-07 10:36:00',
        level: 'DEBUG',
        message: 'SSH-Verbindung geprüft',
    },
    {
        timestamp: '2025-04-07 10:36:55',
        level: 'INFO',
        message: 'Cloudzugriff aktiv',
    },
    {
        timestamp: '2025-04-07 10:37:43',
        level: 'DEBUG',
        message: 'Speichernutzung bei 24%',
    },
    {
        timestamp: '2025-04-07 10:38:30',
        level: 'USER',
        message: 'Log exportiert',
    },
    {
        timestamp: '2025-04-07 10:39:12',
        level: 'ERROR',
        message: 'Prozessabbruch durch Benutzer',
    },
    {
        timestamp: '2025-04-07 10:40:00',
        level: 'INFO',
        message: 'Wartungsmodus aktiviert',
    },
    {
        timestamp: '2025-04-07 10:41:00',
        level: 'USER',
        message: 'Manuelle Prüfung erfolgreich',
    },
]
