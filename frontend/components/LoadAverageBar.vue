<template>
    <div class="space-y-1">
        <!-- Titel + Info -->
        <div class="flex items-center gap-2">
            <p class="text-sm text-muted-foreground">Systemauslastung</p>
            <InfoPopover
                message="Zeigt die durchschnittliche Systemlast pro CPU-Kern über 1, 5 und 15 Minuten.<br>
          Werte über <strong>1.00</strong> bedeuten, dass Prozesse warten müssen."
            />
        </div>

        <!-- Werte -->
        <div class="flex items-center gap-4">
            <span :class="loadBadgeClass(load['1m'])">
                1m: <span class="font-semibold">{{ load['1m'] }}</span>
            </span>
            <span :class="loadBadgeClass(load['5m'])">
                5m: <span class="font-semibold">{{ load['5m'] }}</span>
            </span>
            <span :class="loadBadgeClass(load['15m'])">
                15m: <span class="font-semibold">{{ load['15m'] }}</span>
            </span>
        </div>
    </div>
</template>

<script setup>
import { loadBadgeClass } from '@/utils/statusColors'

const props = defineProps({
    load: {
        type: Object,
        required: true,
    },
})
</script>
