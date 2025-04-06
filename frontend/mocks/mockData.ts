const system = {
    hostname: 'embedded-host',
    time: '2025-04-06 14:22:10',
    uptime: '3 Tage, 4 Stunden',
    load: {
        '1m': 2.97,
        '5m': 1.55,
        '15m': 0.96,
    },
    sd: {
        used: '7.8 GB',
        total: '32 GB',
        percent: 24.4,
    },
}

const network = {
    modem: {
        signal: -72,
        network: 'LTE (Telekom)',
        ip: '10.143.8.21',
    },
    netbird: {
        status: 'Verbunden',
        peer_ip: '100.72.42.12',
        latency: '48ms',
    },
}

const database = {
    size: 120.03,
    created: '2024-08-22 10:15:00',
    updated: '2025-04-06 13:57:23',
}

const containers = [
    {
        name: 'backend',
        image: 'backend:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        name: 'frontend',
        image: 'frontend:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        name: 'fieldcom',
        image: 'fieldcom:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        name: 'gateway',
        image: 'gateway:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        name: 'cellular',
        image: 'cellular:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
    {
        name: 'base',
        image: 'base:latest',
        version: '1.0.0',
        uptime: '2 Tage, 1 Stunde',
        status: 'Läuft',
    },
]

export { system, network, database, containers }
