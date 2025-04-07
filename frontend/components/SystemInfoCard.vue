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

                        <!-- TODO: (i)-Komponente -->
                        <TooltipProvider>
                            <Tooltip>
                                <TooltipTrigger as-child>
                                    <span class="material-icons text-xs text-muted-foreground cursor-help">info</span
                                    >
                                </TooltipTrigger>
                                <TooltipContent class="max-w-xs text-xs leading-relaxed">
                                    Zeigt die durchschnittliche Systemlast pro
                                    CPU-Kern über 1, 5 und 15 Minuten.<br />
                                    Werte über <strong>1.00</strong> bedeuten,
                                    dass Prozesse warten müssen.
                                </TooltipContent>
                            </Tooltip>
                        </TooltipProvider>

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

            <!-- Speichernutzung (SD-Karte) -->
            <div class="mt-6">
                <p class="text-sm text-muted-foreground mb-1">
                    Speichernutzung (SD-Karte)
                </p>

                <div class="w-full bg-muted h-3 rounded overflow-hidden">
                    <div
                        class="h-3 rounded"
                        :class="sdBarColor(system.sd.percent)"
                        :style="`width: ${system.sd.percent}%`"
                    ></div>
                </div>

                <p class="text-xs text-muted-foreground mt-1">
                    {{ system.sd.used }} von {{ system.sd.total }} verwendet ({{
                        system.sd.percent
                    }}%)
                </p>
            </div>

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
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip'
import { loadBadgeClass, sdBarColor } from '@/utils/statusColors'
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
