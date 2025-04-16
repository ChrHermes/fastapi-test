<template>
    <div>
        <div class="flex items-center gap-2 mb-2">
            <span class="material-icons text-base text-muted-foreground"
                >vpn_lock</span
            >
            <p class="text-sm font-semibold text-foreground">VPN-Verbindung</p>
        </div>

        <p class="text-sm">
            Status:
            <span
                :class="vpnBadgeClass(vpn.status)"
                class="ml-1 px-2 py-0.5 rounded text-xs text-white"
            >
                {{ vpn.status }}
            </span>
        </p>
        <p class="text-sm">
            Peer IP: <strong>{{ vpn.peer_ip }}</strong>
        </p>
        <p class="text-sm">
            Version: <strong>{{ vpn.version }}</strong>
        </p>
        <p class="text-sm text-muted-foreground">
            Latenz: {{ formatLatency(vpn.latency) }}
        </p>
    </div>
</template>

<script setup>
const props = defineProps({
    vpn: Object,
})

function vpnBadgeClass(status) {
    return status === 'Verbunden' ? 'bg-green-500' : 'bg-red-500'
}

function formatLatency(latency) {
    return typeof latency === 'number' ? `${latency.toFixed(0)}ms` : latency
}
</script>
