<template>
  <Card class="row-span-1 col-span-1">
    <CardHeader>
      <div class="flex items-center gap-2">
        <span class="material-icons text-base text-muted-foreground">vpn_lock</span>
        <CardTitle class="text-base font-semibold leading-tight">
          VPN-Verbindung
        </CardTitle>
      </div>
    </CardHeader>

    <CardContent class="space-y-1 text-sm">
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
    </CardContent>
  </Card>
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
