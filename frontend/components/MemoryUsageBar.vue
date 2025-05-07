<template>
    <InnerCard title="Arbeitsspeicher">
        <!-- Fortschrittsbalken -->
        <div class="w-full bg-gray-300 h-3 rounded overflow-hidden">
            <div
                class="h-3 rounded bg-blue-500"
                :style="`width: ${usagePercent}%`"
            ></div>
        </div>

        <p class="text-xs text-muted-foreground mt-1">
            {{ formattedUsed }} von {{ formattedTotal }} verwendet ({{
                usagePercent
            }}%)
        </p>
    </InnerCard>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    memory: {
        type: Object,
        required: true,
        // Erwartet: { total: number, available: number } (beide in Bytes)
    },
})

const used = computed(() => props.memory.total - props.memory.available)

const usagePercent = computed(() => {
    if (props.memory.total === 0) return 0
    return ((used.value / props.memory.total) * 100).toFixed(1)
})

function formatBytes(bytes) {
    const gb = bytes / 1024 ** 3
    return `${gb.toFixed(1)} GB`
}

const formattedUsed = computed(() => formatBytes(used.value))
const formattedTotal = computed(() => formatBytes(props.memory.total))
</script>
