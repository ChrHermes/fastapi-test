<template>
    <InnerCard title="Arbeitsspeicher">
      <!-- Fortschrittsbalken mit 4 Farben -->
      <div class="w-full bg-muted h-3 rounded overflow-hidden flex">
        <div
          class="h-3"
          :class="memoryColors.used"
          :style="{ width: usedPercent + '%' }"
          title="Used"
        ></div>
        <div
          class="h-3"
          :class="memoryColors.buffers"
          :style="{ width: buffersPercent + '%' }"
          title="Buffers"
        ></div>
        <div
          class="h-3"
          :class="memoryColors.cached"
          :style="{ width: cachedPercent + '%' }"
          title="Cached"
        ></div>
        <div
          class="h-3"
          :class="memoryColors.free"
          :style="{ width: freePercent + '%' }"
          title="Free"
        ></div>
      </div>
  
      <!-- Legende in zwei Spalten -->
      <ul class="text-xs text-muted-foreground mt-2 grid grid-cols-2 gap-x-4 gap-y-1">
        <li class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded" :class="memoryColors.used"></span>
          Used: {{ formatSmartBytes(usedBytes) }}
        </li>
        <li class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded" :class="memoryColors.buffers"></span>
          Buffers: {{ formatSmartBytes(buffersBytes) }}
        </li>
        <li class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded" :class="memoryColors.cached"></span>
          Cached: {{ formatSmartBytes(cachedBytes) }}
        </li>
        <li class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded" :class="memoryColors.free"></span>
          Free: {{ formatSmartBytes(freeBytes) }}
        </li>
      </ul>
  
      <!-- Gesamtspeicheranzeige -->
      <p class="text-xs text-muted-foreground mt-2 text-center">
        <strong>Gesamt: {{ formatSmartBytes(totalBytes) }}</strong>
      </p>
    </InnerCard>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    memory: {
      type: Object,
      required: true,
      // Struktur: { total_kb, used_kb, buffers_kb, cached_kb, free_kb }
    },
  })
  
  // Farbdefinition zentral
  const memoryColors = {
    used: 'bg-red-500',
    buffers: 'bg-yellow-400',
    cached: 'bg-green-500',
    free: 'bg-blue-500',
  }
  
  // Umwandlung in Bytes
  const toBytes = (kb) => kb * 1024
  
  const totalBytes = computed(() => toBytes(props.memory.total_kb))
  const usedBytes = computed(() => toBytes(props.memory.used_kb))
  const buffersBytes = computed(() => toBytes(props.memory.buffers_kb))
  const cachedBytes = computed(() => toBytes(props.memory.cached_kb))
  const freeBytes = computed(() => toBytes(props.memory.free_kb))
  
  // Prozentwerte
  const usedPercent = computed(() =>
    ((props.memory.used_kb / props.memory.total_kb) * 100).toFixed(1)
  )
  const buffersPercent = computed(() =>
    ((props.memory.buffers_kb / props.memory.total_kb) * 100).toFixed(1)
  )
  const cachedPercent = computed(() =>
    ((props.memory.cached_kb / props.memory.total_kb) * 100).toFixed(1)
  )
  const freePercent = computed(() =>
    ((props.memory.free_kb / props.memory.total_kb) * 100).toFixed(1)
  )
  
  // Dynamische Größenformatierung
  function formatSmartBytes(bytes) {
    const kb = bytes / 1024
    const mb = kb / 1024
    const gb = mb / 1024
  
    if (gb >= 1) return `${gb.toFixed(1)} GB`
    if (mb >= 1) return `${mb.toFixed(1)} MB`
    return `${kb.toFixed(0)} kB`
  }
  </script>
  