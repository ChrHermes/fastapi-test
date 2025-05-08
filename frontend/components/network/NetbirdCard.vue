<template>
    <LayoutInnerCard icon="vpn_lock" title="VPN-Verbindung">
        <p>
            Status:
            <span
                :class="vpnBadgeClass(vpn.status)"
                class="ml-1 px-2 py-0.5 rounded text-xs text-white"
            >
                {{ vpn.status }}
            </span>
        </p>
        <p>
            Peer IP:
            <strong>{{ vpn.peer_ip }}</strong>
        </p>
        <p>
            Version:
            <strong>{{ vpn.version }}</strong>
        </p>
        <p class="text-muted-foreground">
            Latenz: {{ formatLatency(vpn.latency) }}
        </p>
    </LayoutInnerCard>
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
