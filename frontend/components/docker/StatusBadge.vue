<template>
  <span
    :class="badgeClass"
    class="inline-flex items-center gap-1 text-xs font-medium px-2 py-px rounded text-white leading-tight"
    style="line-height: 1.1"
  >
    <span class="material-icons text-[13px] -mb-px leading-none">{{ icon }}</span>
    {{ status }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    status: {
        type: String,
        required: true,
    },
})

const badgeClass = computed(() => {
    switch (props.status) {
        case 'Läuft':
        case 'Verbunden':
            return 'bg-green-500'
        case 'Beendet':
            return 'bg-gray-500'
        case 'Fehler':
            return 'bg-red-600'
        default:
            return 'bg-neutral-500'
    }
})

const icon = computed(() => {
    switch (props.status) {
        case 'Läuft':
        case 'Verbunden':
            return 'check'
        case 'Beendet':
            return 'stop'
        case 'Fehler':
            return 'error'
        default:
            return 'help'
    }
})
</script>
