<template>
    <Card>
        <CardHeader>
            <CardTitle>System</CardTitle>
        </CardHeader>
        <CardContent>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">Hostname</p>
                    <p class="text-base font-medium">{{ system.hostname }}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">Systemzeit</p>
                    <p class="text-base font-medium">{{ system.time }}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">System-Uptime</p>
                    <p class="text-base font-medium">{{ system.uptime }}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">Load Average</p>
                    <div class="flex items-center gap-4">
                        <span :class="loadBadgeClass(system.load['1m'])"
                            >1m: {{ system.load['1m'] }}</span
                        >
                        <span :class="loadBadgeClass(system.load['5m'])"
                            >5m: {{ system.load['5m'] }}</span
                        >
                        <span :class="loadBadgeClass(system.load['15m'])"
                            >15m: {{ system.load['15m'] }}</span
                        >
                    </div>
                </div>
            </div>
            <div class="mt-6">
                <p class="text-sm text-muted-foreground mb-1">
                    SD-Karte Nutzung
                </p>
                <div class="w-full bg-muted h-3 rounded">
                    <div
                        class="bg-primary h-3 rounded"
                        :style="`width: ${system.sd.percent}%`"
                    ></div>
                </div>
                <p class="text-xs text-muted-foreground mt-1">
                    {{ system.sd.used }} von {{ system.sd.total }} verwendet
                </p>
            </div>
            <div class="mt-6 flex flex-wrap gap-4">
                <SecureConfirmDialog
                    title="System herunterfahren?"
                    description="Du bist dabei, das gesamte System herunterzufahren."
                    confirmation-code="shutdown-now"
                    confirm-variant="destructive"
                    variant="destructive"
                    @confirm="$emit('shutdown')"
                >
                    <span class="material-icons text-base mr-1"
                        >power_settings_new</span
                    >
                    Herunterfahren
                </SecureConfirmDialog>

                <ConfirmDialog
                    title="System neustarten?"
                    description="Das System wird neu gestartet. Offene Verbindungen gehen verloren."
                    confirm-variant="destructive"
                    @confirm="$emit('reboot')"
                >
                    <span class="material-icons text-base mr-1"
                        >restart_alt</span
                    >
                    Neustarten
                </ConfirmDialog>
            </div>
        </CardContent>
    </Card>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import SecureConfirmDialog from '@/components/SecureConfirmDialog.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

defineProps({
    system: {
        type: Object,
        required: true,
    },
})

defineEmits(['shutdown'])

function loadBadgeClass(value) {
    if (value > 2.5) return 'bg-red-500 text-white px-2 py-1 rounded text-xs'
    if (value > 1.5) return 'bg-yellow-500 text-white px-2 py-1 rounded text-xs'
    return 'bg-green-500 text-white px-2 py-1 rounded text-xs'
}
</script>
