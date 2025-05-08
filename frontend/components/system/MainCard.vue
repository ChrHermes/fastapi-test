<template>
    <Card>
        <CardSectionHeader icon="device_hub"> System </CardSectionHeader>

        <CardContent>
            <div class="grid gap-6 grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
                <!-- Allgemeines -->
                <SystemGeneralInfoCard
                    :hostname="system.hostname"
                    :time="system.time"
                    :uptime="system.uptime"
                    :short="false"
                />

                <!-- Systemauslastung -->
                <SystemLoadAvgCard :load="system.load" />

                <!-- Memory -->
                <SystemMemoryCard :memory="system.memory" />
                <!-- <MemoryUsageChart :memory="system.memory" /> -->

                <!-- Datenträger -->
                <!-- <DiskUsageCard :disks="system.disk" /> -->
            </div>

            <!-- <DiskUsageDonut :disk="d" v-for="d in system.disk" :key="d.label" /> -->
            <!-- <CpuLoad :cpu="system.cpu"/> -->

            <!-- Neustarten/Herunterfahren -->
            <div class="mt-6 flex flex-wrap gap-4">
                <ConfirmDialog
                    title="System neustarten?"
                    description="Das System wird neu gestartet. Offene Verbindungen gehen verloren."
                    confirm-variant="destructive"
                    icon="restart_alt"
                    text="Neustarten"
                    @confirm="$emit('reboot')"
                />

                <SecureConfirmDialog
                    title="System herunterfahren?"
                    description="Du bist dabei, das gesamte System herunterzufahren."
                    confirmation-code="shutdown-now"
                    confirm-variant="destructive"
                    variant="destructive"
                    icon="power_settings_new"
                    text="Herunterfahren"
                    @confirm="$emit('shutdown')"
                />
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
