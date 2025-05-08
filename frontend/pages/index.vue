<template>
    <div class="p-6 space-y-6">
        <!-- System Info Section -->
        <SystemMainCard
            :system="system"
            @shutdown="shutdownSystem"
            @reboot="rebootSystem"
        />

        <!-- Datenbankverwaltung -->
        <StorageMainCard
            :database="database"
            :disks="system.disk"
            @reset-db="resetDatabase"
        />

        <!-- Netzwerkübersicht -->
        <NetworkMainCard :network="network" />

        <!-- Docker Container Übersicht als Tabelle -->
        <DockerMainCard :containers="containers" />

        <!-- Protokollanzeige -->
        <LogMainCard :logs="logs" />
    </div>
</template>

<script setup>
import { useMockData } from '@/composables/useMockData'
import { ref, inject, watchEffect, onMounted } from 'vue'
import { toast } from 'vue-sonner'

const refreshTrigger = inject('refreshTrigger')
const autoRefreshEnabled = inject('autoRefreshEnabled')
const loading = inject('loading')

const { system, network, database, containers, logs } = useMockData()
// onMounted(async () => {
//   loading.value = true
//   try {
//     const data = await useData()
//     system.value = data.system
//     network.value = data.network
//     database.value = data.database
//     containers.value = data.containers
//     logs.value = data.logs
//   } finally {
//     loading.value = false
//   }
// })

definePageMeta({
    middleware: 'auth',
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
    toast('Event has been created', {
        description: 'System wird in 10 Sekunden heruntergefahren.',
        action: {
            label: 'Undo',
            onClick: () => console.log('Undo'),
        },
    })
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
