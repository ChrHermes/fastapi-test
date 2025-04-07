<template>
    <Dialog :open="open" @update:open="emit('update:open', $event)">
      <DialogContent class="max-w-3xl">
        <DialogHeader>
          <DialogTitle>
            Container-Details: <span class="font-mono">{{ container?.name }}</span>
          </DialogTitle>
        </DialogHeader>
  
        <!-- Details -->
        <div
          class="grid grid-cols-2 gap-2 text-xs text-muted-foreground border rounded p-3 bg-muted/50 mb-4"
        >
          <p>
            <span class="font-medium text-foreground">ID:</span>
            {{ container?.id }}
          </p>
          <p>
            <span class="font-medium text-foreground">Status:</span>
            {{ container?.status }}
          </p>
          <p>
            <span class="font-medium text-foreground">Version:</span>
            {{ container?.version }}
          </p>
          <p>
            <span class="font-medium text-foreground">Laufzeit:</span>
            {{ container?.uptime }}
          </p>
          <p class="col-span-2">
            <span class="font-medium text-foreground">Image:</span>
            {{ container?.image }}
          </p>
        </div>
  
        <!-- Logs-Überschrift & Auto-Refresh Toggle -->
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-bold text-muted-foreground">Container-Logs</h3>
          <Button
            variant="outline"
            size="sm"
            class="gap-2 text-xs"
            @click="toggleAutoRefresh"
          >
            <span class="material-icons text-base">autorenew</span>
            <span v-if="autoRefresh">
              Auto-Refresh ({{ secondsLeft }} s)
            </span>
            <span v-else> Auto-Refresh aktivieren </span>
          </Button>
        </div>
  
        <!-- Logs -->
        <div
        class="h-64 overflow-auto text-xs bg-background border rounded p-2 font-mono leading-relaxed"
        >
        <div
            v-for="(line, i) in logs"
            :key="i"
            :class="[
            'text-muted-foreground whitespace-pre-wrap break-words px-2 py-1 rounded',
            i % 2 === 0 ? 'bg-muted/30' : ''
            ]"
        >
            {{ line }}
        </div>

        </div>
      </DialogContent>
    </Dialog>
  </template>
  
  <script setup>
  import { ref, watch, onBeforeUnmount } from 'vue'
  import {
      Dialog,
      DialogContent,
      DialogHeader,
      DialogTitle,
  } from '@/components/ui/dialog'
  import { Button } from '@/components/ui/button'
  
  const props = defineProps({
      container: Object,
      open: Boolean,
  })
  
  const emit = defineEmits(['update:open'])
  
  // Konfiguration
  const pollInterval = 5 // Sekunden zwischen Auto-Refresh
  const logCount = 10    // Anzahl der Logzeilen
  
  const autoRefresh = ref(false)
  const secondsLeft = ref(pollInterval)
  const logs = ref([])
  
  let countdownId = null
  
  async function fetchLogs() {
      if (!props.container?.name) return
      console.log('[MOCK] Lade Container-Logs für:', props.container.name)
      logs.value = Array.from(
          { length: logCount },
          (_, i) => `[${new Date().toISOString()}] Logzeile ${i + 1}`
      )
  }
  
  function toggleAutoRefresh() {
      autoRefresh.value = !autoRefresh.value
  
      if (autoRefresh.value) {
          secondsLeft.value = pollInterval
          fetchLogs()
  
          countdownId = setInterval(() => {
              secondsLeft.value--
              if (secondsLeft.value <= 0) {
                  fetchLogs()
                  secondsLeft.value = pollInterval
              }
          }, 1000)
      } else {
          clearInterval(countdownId)
          countdownId = null
      }
  }
  
  // Automatisches Laden beim Öffnen des Modals (sobald Container da ist)
  watch(
      () => [props.open, props.container],
      async ([isOpen, container]) => {
          if (isOpen && container?.name) {
              await fetchLogs()
          } else {
              autoRefresh.value = false
              clearInterval(countdownId)
          }
      },
      { immediate: true }
  )
  
  onBeforeUnmount(() => clearInterval(countdownId))
  </script>
  