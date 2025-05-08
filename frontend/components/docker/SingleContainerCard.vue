<template>
    <LayoutInnerCard icon="inventory_2" :title="container.name">
        <div class="space-y-1 text-sm text-muted-foreground">
            <!-- Erste Zeile: Status (links untenbündig), Details-Button (rechts oben) -->
            <div class="flex justify-between items-end">
                <div class="flex items-end gap-2">
                    <span class="text-foreground">Status:</span>
                    <DockerStatusBadge :status="container.status" />
                </div>

                <button
                    class="text-muted-foreground hover:text-primary transition-colors text-xs inline-flex items-center gap-1"
                    @click="$emit('info', container)"
                >
                    <span class="material-icons text-sm">info</span>
                    Details
                </button>
            </div>

            <!-- Version -->
            <div>
                <span class="text-foreground">Version: </span>
                <span class="font-semibold text-foreground">{{
                    container.version
                }}</span>
            </div>

            <!-- Uptime -->
            <div>
                <span class="text-foreground">Laufzeit: </span>
                <span class="font-semibold text-foreground">{{
                    container.uptime
                }}</span>
            </div>
        </div>
    </LayoutInnerCard>
</template>

<script setup>
defineProps({
    container: {
        type: Object,
        required: true,
    },
})
</script>
