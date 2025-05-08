<template>
    <Card>
        <CardSectionHeader icon="storage">Speicherverwaltung</CardSectionHeader>
        <CardContent>
            <div class="grid gap-6 grid-cols-1 md:grid-cols-2">
                <DiskUsageCard :disks="disks" />
                <DatabaseInfo :database="database" @reset-db="$emit('reset-db')" />

            </div>
        </CardContent>
    </Card>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'

defineProps({
    database: {
        type: Object,
        required: true,
    },
    disks: {
        type: Object,
        required: true,
    },
})

defineEmits(["reset-db"]);

</script>
