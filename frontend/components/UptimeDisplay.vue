<!-- components/system/UptimeDisplay.vue -->
<template>
    <div class="space-y-1">
        <p class="text-sm text-muted-foreground">Laufzeit seit Start</p>
        <p class="text-base font-medium">
            <span v-if="short">
                {{ uptime.days }}d {{ uptime.hours }}h {{ uptime.minutes }}m
            </span>
            <span v-else>
                {{ uptime.days }} Tage, {{ uptime.hours }}:{{
                    padded(uptime.minutes)
                }}
                Stunden
            </span>
        </p>
    </div>
</template>

<script setup>
const props = defineProps({
    uptime: {
        type: Object,
        required: true,
        validator: (obj) => ['days', 'hours', 'minutes'].every((k) => k in obj),
    },
    short: {
        type: Boolean,
        default: false,
    },
})

function padded(n) {
    return String(n).padStart(2, '0')
}
</script>
