<template>
  <Card>
    <CardSectionHeader icon="wifi" subtitle="Modem & VPN-Verbindung">
      Netzwerk
    </CardSectionHeader>

    <CardContent>
      <div class="grid gap-6 grid-cols-1 sm:grid-cols-2">
        <ModemInfo :modem="network.modem" />
        <NetbirdInfo :vpn="network.netbird" />
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'

const props = defineProps({
  network: {
    type: Object,
    required: true,
  },
})
</script>
