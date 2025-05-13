<template>
    <LayoutInnerCard icon="mobiledata_off" title="Netzwerkinterface">
        <!-- Name und Status als Listen-Eintrag -->
        <p class="">
            <span>
                Name: <strong>{{ iface.interface }}</strong>
            </span>
            <span
                :class="badgeClass(iface.operstate)"
                class="ml-2 px-2 py-0.5 rounded text-xs text-white"
            >
            {{ readableStatus(iface.operstate) }}
        </span>
        </p>

        <!-- MAC-Adresse dezenter -->
        <p class="text-muted-foreground">
            MAC-Adresse: {{ iface.mac }}
        </p>

        <p class="">
            IP-Adresse: <strong>{{ iface.ip }}</strong>
        </p>
        <p class="">
            Gateway: <strong>{{ iface.gateway }}</strong>
        </p>
        <p>
            Netzmaske: <strong>{{ iface.netmask }}</strong>
        </p>

        <!-- RX/TX nebeneinander, dezenter Text mit Symbol -->
        <div
            class="flex items-center text-muted-foreground space-x-4"
        >
            <span class="flex items-center space-x-1">
                <span class="material-icons text-sm">download</span>
                <span>{{ formatBytes(iface.rx_bytes) }}</span>
            </span>
            <span class="flex items-center space-x-1">
                <span class="material-icons text-sm">upload</span>
                <span>{{ formatBytes(iface.tx_bytes) }}</span>
            </span>
        </div>
    </LayoutInnerCard>
</template>

<script setup>
const props = defineProps({
    iface: {
        type: Object,
        required: true,
        // Erwartete Felder:
        // interface, operstate, mac, ip, gateway, netmask, rx_bytes, tx_bytes
    },
})

// Mapping für lesbare Status-Bezeichnungen
const statusMap = {
    up: 'Aktiv',
    down: 'Inaktiv',
    unknown: 'Unbekannt',
}

function readableStatus(status) {
    return statusMap[status] || status
}

function badgeClass(status) {
    return status === 'up' ? 'bg-green-500' : 'bg-red-500'
}

function formatBytes(bytes) {
    if (typeof bytes !== 'number') return bytes
    const units = ['B', 'KB', 'MB', 'GB', 'TB']
    let u = 0
    let value = bytes
    while (value >= 1024 && u < units.length - 1) {
        value /= 1024
        u++
    }
    return `${value.toFixed(1)} ${units[u]}`
}
</script>
