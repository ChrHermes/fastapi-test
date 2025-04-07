<template>
    <div class="p-6 space-y-6">
        <!-- System Info Section -->
        <SystemInfoCard
            :system="system"
            @shutdown="shutdownSystem"
            @reboot="rebootSystem"
        />

        <!-- Netzwerkübersicht -->
        <NetworkInfoCard :network="network" />

        <!-- Docker Container Übersicht als Tabelle -->
        <DockerContainerTable :containers="containers" />

        <!-- Datenbankverwaltung -->
        <DatabaseInfoCard :database="database" @reset="resetDatabase" />
    </div>
</template>

<script setup>
import { useMockData } from '@/composables/useMockData'
import { inject, watchEffect } from 'vue'

const refreshTrigger = inject('refreshTrigger')
const autoRefreshEnabled = inject('autoRefreshEnabled')
const { system, network, database, containers } = useMockData()

definePageMeta({
  middleware: 'auth'
})

watchEffect(() => {
  if (autoRefreshEnabled?.value) {
    refreshTrigger?.value
    console.log('Mockdaten-Refresh ausgelöst')
  }
})

function shutdownSystem() {
  console.log('System wird heruntergefahren')
  // TODO: API call to /api/system/shutdown
}

function rebootSystem() {
  console.log('System wird neugestartet')
  // TODO: API call to /api/system/reboot
}

function resetDatabase() {
  console.log('Datenbank wird zurückgesetzt')
  // TODO: API call to /api/database/reset
}
</script>
