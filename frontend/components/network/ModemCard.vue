<!-- components/cards/ModemCard.vue -->
<template>
    <LayoutInnerCard icon="signal_cellular_alt" title="Mobilfunkmodem">
        <p>
            Netz:
            <strong>{{ modem.carrier }}</strong>
            <span
                :class="modemTypeBadgeClass(modem.network)"
                class="ml-2 px-2 py-0.5 rounded text-xs text-white"
            >
                {{ modemTypeLabel(modem.network) }}
            </span>
        </p>

        <p>
            IP:
            <strong>{{ modem.ip }}</strong>
        </p>

        <div class="flex items-end gap-1 h-6 mt-4 mb-1">
            <div
                v-for="i in 5"
                :key="i"
                class="w-1.5 rounded"
                :class="signalBarColor(i)"
                :style="{ height: `${i * 0.4}rem` }"
            />
        </div>

        <p class="text-xs text-muted-foreground flex items-center gap-1">
            Signal: {{ modem.signal }} dBm
            <CommonInfoPopover
                class="ml-1"
                message="Signalstärke in dBm. Werte über -60 dBm gelten als sehr gut, unter -90 dBm als schwach. Die Balken zeigen die Qualität an."
            />
        </p>
    </LayoutInnerCard>
</template>

<script setup>

const props = defineProps({
    modem: Object,
})

const signalLevel = computed(() => {
    const dbm = props.modem.signal
    if (dbm >= -60) return 5
    if (dbm >= -70) return 4
    if (dbm >= -80) return 3
    if (dbm >= -90) return 2
    return 1
})

function signalBarColor(i) {
    const active = signalLevel.value >= i
    if (!active) return 'bg-muted'
    return signalLevel.value <= 2
        ? 'bg-red-500'
        : signalLevel.value === 3
        ? 'bg-yellow-500'
        : 'bg-green-500'
}

function modemTypeLabel(type) {
    if (type.includes('LTE')) return 'LTE'
    if (type.includes('GPRS')) return 'GPRS'
    return 'EDGE'
}

function modemTypeBadgeClass(type) {
    if (type.includes('LTE')) return 'bg-green-500'
    if (type.includes('GPRS')) return 'bg-yellow-500'
    return 'bg-red-500'
}
</script>
