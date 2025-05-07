<template>
    <InnerCard title="Allgemeines">
        <ul class="text-sm text-foreground space-y-1">
            <li>Gerätename: <strong>{{ hostname }}</strong></li>
            <li>Laufzeit seit Start: <strong>{{ uptimeText }}</strong></li>
            <li>Aktuelle Systemzeit: <strong>{{ time }}</strong></li>
        </ul>
    </InnerCard>
</template>

<script setup>
const props = defineProps({
    hostname: { type: String, required: true },
    time: { type: String, required: true },
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

// Hilfsfunktion zum Formatieren
function padded(n) {
  return String(n).padStart(2, '0')
}

// Uptime-Text vorbereiten
const uptimeText = computed(() => {
  const { days, hours, minutes } = props.uptime
  if (props.short) {
    return `${days}d ${hours}h ${minutes}m`
  }
  return `${days} Tage, ${hours}:${padded(minutes)} Stunden`
})

</script>
