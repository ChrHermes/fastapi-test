<template>
    <Card>
        <CardSectionHeader icon="memory">System</CardSectionHeader>

        <CardContent>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">Gerätename</p>
                    <p class="text-base font-medium">{{ system.hostname }}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">Systemzeit</p>
                    <p class="text-base font-medium">{{ system.time }}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-muted-foreground">
                        Laufzeit seit Start
                    </p>
                    <p class="text-base font-medium">{{ system.uptime }}</p>
                </div>

                <!-- Systemauslastung -->
                <div class="space-y-1">
                    <div class="flex items-center gap-2">
                        <p class="text-sm text-muted-foreground">
                            Systemauslastung
                        </p>

                        <InfoPopover
                            message="Zeigt die durchschnittliche Systemlast pro CPU-Kern über 1, 5 und 15 Minuten. <br>
                            Werte über <strong>1.00</strong> bedeuten, dass Prozesse warten müssen."
                        />
                    </div>

                    <div class="flex items-center gap-4">
                        <span :class="loadBadgeClass(system.load['1m'])">
                            1m:
                            <span class="font-semibold">{{
                                system.load['1m']
                            }}</span>
                        </span>
                        <span :class="loadBadgeClass(system.load['5m'])">
                            5m:
                            <span class="font-semibold">{{
                                system.load['5m']
                            }}</span>
                        </span>
                        <span :class="loadBadgeClass(system.load['15m'])">
                            15m:
                            <span class="font-semibold">{{
                                system.load['15m']
                            }}</span>
                        </span>
                    </div>
                </div>
            </div>

            <!-- Datenträger -->
            <DiskUsageBar
                v-for="disk in system.disk"
                :key="disk.label"
                :label="disk.label"
                :used="disk.used"
                :total="disk.total"
                :percent="disk.percent"
            />

            <!-- Neustarten/Herunterfahren -->
            <div class="mt-6 flex flex-wrap gap-4">
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
            </div>
        </CardContent>
    </Card>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'
import { loadBadgeClass } from '@/utils/statusColors'
import SecureConfirmDialog from '@/components/SecureConfirmDialog.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

defineProps({
    system: {
        type: Object,
        required: true,
    },
})

defineEmits(['shutdown'])
</script>
