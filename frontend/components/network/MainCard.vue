<template>
  <Card>
    <LayoutCardSectionHeader icon="wifi" subtitle="Modem & VPN-Verbindung">
      Netzwerk
    </LayoutCardSectionHeader>

    <CardContent>
      <div class="grid gap-6 grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
        <NetworkInterfaceCard :iface="network.interface" />
        <NetworkModemCard :modem="network.modem" />
        <NetworkNetbirdCard :vpn="network.netbird" />
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
