<template>
    <Card>
        <CardSectionHeader icon="memory"> System </CardSectionHeader>

        <CardContent>
            <div class="grid gap-6 grid-cols-1 sm:grid-cols-3">


                <GeneralSystemInfo
                    :hostname="system.hostname"
                    :time="system.time"
                    :uptime="system.uptime"
                    :short="false"
                />


                <!-- Systemauslastung -->
                <LoadAverageBar :load="system.load" />

                <!-- Memory -->
                <MemoryUsageBar :memory="system.memory" />
            </div>

            <MemoryUsageChart :memory="system.memory" />
            <!-- <DiskUsageDonut :disk="d" v-for="d in system.disk" :key="d.label" /> -->
            <!-- <CpuLoad :cpu="system.cpu"/> -->

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

defineProps({
    system: {
        type: Object,
        required: true,
    },
})

defineEmits(['shutdown'])
</script>
