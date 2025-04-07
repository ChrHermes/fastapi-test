<template>
  <Card>
    <CardSectionHeader icon="wifi" subtitle="Modem & VPN-Verbindung">
      Netzwerk
    </CardSectionHeader>

    <CardContent>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Modem -->
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="material-icons text-base text-muted-foreground">signal_cellular_alt</span>
            <p class="text-sm font-semibold text-foreground">Mobilfunkmodem</p>
          </div>

          <!-- Netz & IP -->
          <p class="text-sm">
            Netz: <strong>{{ network.modem.carrier }}</strong>
            <span :class="modemTypeBadgeClass(network.modem.network)"
              class="ml-2 px-2 py-0.5 rounded text-xs text-white">
              {{ modemTypeLabel(network.modem.network) }}
            </span>
          </p>
          <p class="text-sm">IP: <strong>{{ network.modem.ip }}</strong></p>

          <!-- Signalstärke -->
          <div class="flex items-end gap-1 h-6 mt-2 mb-1">
            <div v-for="i in 5" :key="i" class="w-1.5 rounded" :class="signalBarColor(i)"
              :style="{ height: `${i * 0.4}rem` }" />
          </div>
          <p class="text-xs text-muted-foreground mb-2">Signal: {{ network.modem.signal }} dBm</p>
        </div>

        <!-- NetBird / VPN -->
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="material-icons text-base text-muted-foreground">vpn_lock</span>
            <p class="text-sm font-semibold text-foreground">VPN-Verbindung</p>
          </div>

          <p class="text-sm">
            Status:
            <span :class="vpnBadgeClass(network.netbird.status)" class="ml-1 px-2 py-0.5 rounded text-xs text-white">
              {{ network.netbird.status }}
            </span>
          </p>
          <p class="text-sm">Peer IP: <strong>{{ network.netbird.peer_ip }}</strong></p>
          <p class="text-sm">Version: <strong>{{ network.netbird.version }}</strong></p>
          <p class="text-sm text-muted-foreground">Latenz: {{ formatLatency(network.netbird.latency) }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'
import CardSectionHeader from '@/components/CardSectionHeader.vue'
import { computed } from 'vue'

const props = defineProps({
  network: {
    type: Object,
    required: true,
  },
})

// Balkenanzahl (1–5)
const signalLevel = computed(() => {
  const dbm = props.network.modem.signal
  if (dbm >= -60) return 5
  if (dbm >= -70) return 4
  if (dbm >= -80) return 3
  if (dbm >= -90) return 2
  return 1
})

// Balkenfarbe je Stufe
function signalBarColor(i) {
  const active = signalLevel.value >= i
  if (!active) return 'bg-muted'

  return signalLevel.value <= 2
    ? 'bg-red-500'
    : signalLevel.value === 3
      ? 'bg-yellow-500'
      : 'bg-green-500'
}

// Badge Netztyp
function modemTypeLabel(networkStr) {
  if (networkStr.includes('LTE')) return 'LTE'
  if (networkStr.includes('GPRS')) return 'GPRS'
  return 'EDGE'
}

function modemTypeBadgeClass(networkStr) {
  if (networkStr.includes('LTE')) return 'bg-green-500'
  if (networkStr.includes('GPRS')) return 'bg-yellow-500'
  return 'bg-red-500' // z. B. EDGE oder unbekannt
}

// Badge VPN-Status
function vpnBadgeClass(status) {
  return status === 'Verbunden' ? 'bg-green-500' : 'bg-red-500'
}

// Latenz (sicheres Format)
function formatLatency(latency) {
  return typeof latency === 'number' ? `${latency.toFixed(0)}ms` : latency
}
</script>
