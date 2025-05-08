<template>
    <div class="space-y-1">
      <p class="text-sm text-muted-foreground flex items-center gap-2">
        CPU-Last
      </p>
  
      <!-- Load Averages -->
      <div class="flex items-center gap-4">
        <span :class="loadBadgeClass(cpu['1m'])">
          1m:
          <span class="font-semibold">{{ cpu['1m'] }}</span>
        </span>
        <span :class="loadBadgeClass(cpu['5m'])">
          5m:
          <span class="font-semibold">{{ cpu['5m'] }}</span>
        </span>
        <span :class="loadBadgeClass(cpu['15m'])">
          15m:
          <span class="font-semibold">{{ cpu['15m'] }}</span>
        </span>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    cpu: {
      type: Object,
      required: true,
      // Erwartet: { "1m": float, "5m": float, "15m": float }
    }
  })
  
  function loadBadgeClass(value) {
    if (value > 2.0) return 'bg-red-500 text-white text-xs px-2 py-0.5 rounded'
    if (value > 1.0) return 'bg-yellow-500 text-black text-xs px-2 py-0.5 rounded'
    return 'bg-green-500 text-white text-xs px-2 py-0.5 rounded'
  }
  </script>
  