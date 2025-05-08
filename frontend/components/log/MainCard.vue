<template>
    <Card>
        <CardSectionHeader icon="receipt_long">Protokoll</CardSectionHeader>

        <CardContent class="space-y-4">
            <!-- Logs -->
            <div ref="logContainer"
                class="h-64 overflow-auto bg-muted rounded px-4 py-3 text-sm space-y-1 leading-relaxed">
                <div v-for="(log, index) in filteredLogs" :key="index"
                    class="whitespace-pre-wrap text-muted-foreground">
                    <!-- Timestamp -->
                    <span class="inline-block w-[140px] text-xs text-foreground">{{ log.timestamp }}</span>

                    <!-- Loglevel -->
                    <span v-if="showLevelBadges" :class="levelClass(log.level)"
                        class="inline-block text-center px-2 py-0.5 rounded text-xs w-16">
                        {{ log.level }}
                    </span>
                    <span v-else class="text-xs text-muted-foreground font-medium mr-2 inline-block w-16 text-center">
                        {{ log.level }}
                    </span>

                    <!-- Message -->
                    <span class="pl-2">{{ log.message }}</span>

                    <!-- Scroll-Ziel -->
                    <div ref="scrollAnchor"></div>
                </div>
            </div>

            <!-- Einstellungen -->
            <div class="flex flex-wrap items-center justify-between gap-4 text-xs text-muted-foreground pt-4 border-t">
                <!-- Loglevel -->
                <div class="flex items-center gap-2">
                    <label for="logLevel">Log-Level:</label>
                    <select id="logLevel" v-model="selectedLevel"
                        class="px-2 py-1 bg-background border border-muted rounded text-xs">
                        <option value="">Alle</option>
                        <option v-for="level in levels" :key="level" :value="level">{{ level }}</option>
                    </select>
                </div>

                <!-- Zeilenlimit -->
                <div class="flex items-center gap-2">
                    <label for="lineLimit">Limit:</label>
                    <select id="lineLimit" v-model="lineLimit"
                        class="px-2 py-1 bg-background border border-muted rounded text-xs">
                        <option v-for="n in limits" :key="n" :value="n">{{ n }} Zeilen</option>
                    </select>
                </div>

                <!-- Farben-Toggle -->
                <div class="flex items-center gap-2">
                    <label>Farben:</label>
                    <Button size="sm" variant="outline" @click="toggleBadges"
                        :class="showLevelBadges ? 'bg-primary text-white' : 'text-muted-foreground'">
                        {{ showLevelBadges ? 'An' : 'Aus' }}
                    </Button>
                </div>
            </div>

            <!-- Logeintrag hinzufügen -->
            <div class="pt-2">
                <LogAddEntryDialog @submit="addLogEntry" />
            </div>
        </CardContent>
    </Card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

const props = defineProps({
    logs: {
        type: Array,
        required: true,
    },
})

const logsLocal = ref([...props.logs])
const selectedLevel = ref('')
const lineLimit = ref(20)
const showLevelBadges = ref(false)

const levels = ['INFO', 'ERROR', 'DEBUG', 'USER']
const limits = [20, 50, 100]
const logContainer = ref(null)
const scrollAnchor = ref(null)

watch(logsLocal, () => {
    nextTick(() => {
        // if (logContainer.value) {
        //     logContainer.value.scrollTop = logContainer.value.scrollHeight
        // }
        scrollAnchor.value?.scrollIntoView({ behavior: 'auto' })
    })
})

const filteredLogs = computed(() => {
    return logsLocal.value
        .filter(log => !selectedLevel.value || log.level === selectedLevel.value)
        .slice(-lineLimit.value)
})

function levelClass(level) {
    const base = 'text-white text-xs rounded px-2 py-0.5'
    switch (level) {
        case 'ERROR':
            return `${base} bg-red-500`
        case 'INFO':
            return `${base} bg-blue-500`
        case 'DEBUG':
            return `${base} bg-gray-500`
        case 'USER':
            return `${base} bg-green-600`
        default:
            return `${base} bg-neutral-500`
    }
}

function toggleBadges() {
    showLevelBadges.value = !showLevelBadges.value
}

async function addLogEntry(entry) {
    entry.timestamp = formatTimestamp(new Date())
    logsLocal.value.push(entry)
    await sendLogToBackend(entry)
}

function formatTimestamp(date) {
    const pad = (n) => n.toString().padStart(2, '0')
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

// Lokaler Mock
async function sendLogToBackend(entry) {
    console.log('[MOCK] Sende Logeintrag:', entry)
    await new Promise(resolve => setTimeout(resolve, 300))
}
</script>