<template>
    <Card>
      <CardHeader>
        <CardTitle>Netzwerk</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm text-muted-foreground mb-1">Modem</p>
            <p class="text-sm text-muted-foreground">Signalstärke</p>
            <div class="flex items-center gap-2 mb-2">
              <div class="h-3 w-20 bg-gray-200 rounded">
                <div
                  class="h-3 rounded bg-green-500"
                  :style="`width: ${Math.max(0, Math.min(100, 100 + network.modem.signal))}%`"
                ></div>
              </div>
              <span class="text-xs text-muted-foreground">{{ network.modem.signal }} dBm</span>
            </div>
            <p class="text-sm">Netz: <strong>{{ network.modem.network }}</strong></p>
            <p class="text-sm">IP: <strong>{{ network.modem.ip }}</strong></p>
          </div>
  
          <div>
            <p class="text-sm text-muted-foreground mb-1">NetBird</p>
            <p class="text-sm">Status: <strong>{{ network.netbird.status }}</strong></p>
            <p class="text-sm">Peer IP: <strong>{{ network.netbird.peer_ip }}</strong></p>
            <p class="text-sm text-muted-foreground">Latenz: {{ network.netbird.latency }}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  </template>
  
  <script setup>
  import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
  
  defineProps({
    network: {
      type: Object,
      required: true,
    },
  })

  </script>
  