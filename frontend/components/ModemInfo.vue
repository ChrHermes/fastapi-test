<template>
    <div>
      <div class="flex items-center gap-2 mb-2">
        <span class="material-icons text-base text-muted-foreground">signal_cellular_alt</span>
        <p class="text-sm font-semibold text-foreground">Mobilfunkmodem</p>
      </div>
  
      <p class="text-sm">
        Netz: <strong>{{ modem.carrier }}</strong>
        <span :class="modemTypeBadgeClass(modem.network)" class="ml-2 px-2 py-0.5 rounded text-xs text-white">
          {{ modemTypeLabel(modem.network) }}
        </span>
      </p>
      <p class="text-sm">IP: <strong>{{ modem.ip }}</strong></p>
  
      <div class="flex items-end gap-1 h-6 mt-4 mb-1">
        <div
          v-for="i in 5"
          :key="i"
          class="w-1.5 rounded"
          :class="signalBarColor(i)"
          :style="{ height: `${i * 0.4}rem` }"
        />
      </div>
  
      <p class="text-xs text-muted-foreground mb-2 flex items-center gap-1">
        Signal: {{ modem.signal }} dBm
        <InfoPopover
          class="ml-1"
          message="Signalstärke in dBm. Werte über -60 dBm gelten als sehr gut, unter -90 dBm als schwach. Die Balken zeigen die Qualität an."
        />
      </p>
    </div>
  </template>
  
  <script setup>
  import InfoPopover from '@/components/InfoPopover.vue'
  
  const props = defineProps({
    modem: Object,
  })
  
  const signalLevel = computed(() => {
    const dbm = props.modem.signal
    if (dbm >= -60) return 5
    if (dbm >= -70) return 4
    if (dbm >= -80) return 3
    if (dbm >= -90) return 2
    return 1
  })
  
  function signalBarColor(i) {
    const active = signalLevel.value >= i
    if (!active) return 'bg-muted'
    return signalLevel.value <= 2 ? 'bg-red-500' : signalLevel.value === 3 ? 'bg-yellow-500' : 'bg-green-500'
  }
  
  function modemTypeLabel(type) {
    if (type.includes('LTE')) return 'LTE'
    if (type.includes('GPRS')) return 'GPRS'
    return 'EDGE'
  }
  
  function modemTypeBadgeClass(type) {
    if (type.includes('LTE')) return 'bg-green-500'
    if (type.includes('GPRS')) return 'bg-yellow-500'
    return 'bg-red-500'
  }
  </script>
  