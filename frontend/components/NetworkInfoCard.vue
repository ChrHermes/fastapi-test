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

          <!-- Netz und IP oben -->
          <p class="text-sm">Netz: <strong>{{ network.modem.network }}</strong></p>
          <p class="text-sm">IP: <strong>{{ network.modem.ip }}</strong></p>

          <!-- Signalbalken darunter -->
          <div class="flex items-end gap-1 h-6 mt-2 mb-1">
            <div v-for="i in 5" :key="i" class="w-1.5 rounded" :class="{
              'bg-green-500': signalLevel >= i,
              'bg-muted': signalLevel < i
            }" :style="{ height: `${i * 0.4}rem` }" />
          </div>
          <p class="text-xs text-muted-foreground mb-2">Signal: {{ network.modem.signal }} dBm</p>
        </div>


        <!-- NetBird / VPN -->
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="material-icons text-base text-muted-foreground">vpn_lock</span>
            <p class="text-sm font-semibold text-foreground">VPN-Verbindung</p>
          </div>

          <p class="text-sm">Status: <strong>{{ network.netbird.status }}</strong></p>
          <p class="text-sm">Peer IP: <strong>{{ network.netbird.peer_ip }}</strong></p>
          <p class="text-sm">Version: <strong>{{ network.netbird.version }}</strong></p>
          <p class="text-sm text-muted-foreground">Latenz: {{ network.netbird.latency }}</p>
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

const signalLevel = computed(() => {
  const dbm = props.network.modem.signal
  if (dbm >= -60) return 5
  if (dbm >= -70) return 4
  if (dbm >= -80) return 3
  if (dbm >= -90) return 2
  return 1
})
</script>
