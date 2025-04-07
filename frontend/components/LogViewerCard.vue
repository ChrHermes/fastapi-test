<template>
    <Card>
      <CardHeader>
        <CardTitle>Protokoll</CardTitle>
      </CardHeader>
  
      <CardContent class="space-y-4">
        <!-- Logs -->
        <div class="h-64 overflow-auto bg-muted rounded px-4 py-3 text-sm space-y-1 leading-relaxed">
          <div
            v-for="(log, index) in filteredLogs"
            :key="index"
            class="whitespace-pre-wrap text-muted-foreground"
          >
            <span class="text-xs text-foreground mr-2">[{{ log.timestamp }}]</span>
            <span v-if="showLevelBadges" :class="levelClass(log.level)" class="px-2 py-0.5 rounded text-xs">
              {{ log.level }}
            </span>
            <span v-else class="text-xs text-muted-foreground font-medium mr-2">{{ log.level }}</span>
            {{ log.message }}
          </div>
        </div>
  
        <!-- Einstellungen -->
        <div class="flex flex-wrap items-center justify-between gap-4 text-sm text-muted-foreground">
          <!-- Loglevel -->
          <div class="flex items-center gap-2">
            <label for="logLevel">Log-Level:</label>
            <select
              id="logLevel"
              v-model="selectedLevel"
              class="px-2 py-1 bg-background border rounded text-sm"
            >
              <option value="">Alle</option>
              <option v-for="level in levels" :key="level" :value="level">{{ level }}</option>
            </select>
          </div>
  
          <!-- Zeilenlimit -->
          <div class="flex items-center gap-2">
            <label for="lineLimit">Limit:</label>
            <select
              id="lineLimit"
              v-model="lineLimit"
              class="px-2 py-1 bg-background border rounded text-sm"
            >
              <option v-for="n in limits" :key="n" :value="n">{{ n }} Zeilen</option>
            </select>
          </div>
  
          <!-- Farben-Toggle -->
          <div class="flex items-center gap-2">
            <label for="colorToggle">Farben:</label>
            <input
              id="colorToggle"
              type="checkbox"
              v-model="showLevelBadges"
              class="accent-primary"
            />
          </div>
        </div>
      </CardContent>
    </Card>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
  
  const props = defineProps({
    logs: {
      type: Array,
      required: true,
    },
  })
  
  const selectedLevel = ref('')
  const lineLimit = ref(50)
  const showLevelBadges = ref(false)
  
  const levels = ['INFO', 'ERROR', 'DEBUG', 'USER']
  const limits = [20, 50, 100]
  
  const filteredLogs = computed(() => {
    return props.logs
      .filter(log => !selectedLevel.value || log.level === selectedLevel.value)
      .slice(-lineLimit.value)
  })
  
  function levelClass(level) {
    const base = 'text-white text-xs rounded px-2 py-0.5'
    switch (level) {
      case 'ERROR': return `${base} bg-red-500`
      case 'INFO': return `${base} bg-blue-500`
      case 'DEBUG': return `${base} bg-gray-500`
      case 'USER': return `${base} bg-green-600`
      default: return `${base} bg-neutral-500`
    }
  }
  </script>
  