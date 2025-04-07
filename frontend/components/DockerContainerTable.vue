<template>
    <Card>
        <CardHeader>
            <CardTitle>Laufende Docker Container</CardTitle>
        </CardHeader>
        <CardContent>
            <div class="overflow-auto">
                <table class="w-full text-sm text-left">
                    <thead class="text-muted-foreground">
                        <tr>
                            <th class="px-4 py-2">Name</th>
                            <!-- <th class="px-4 py-2">Image</th> -->
                            <th class="px-4 py-2">Version</th>
                            <th class="px-4 py-2">Uptime</th>
                            <th class="px-4 py-2">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="container in containers"
                            :key="container.name"
                            class="border-t"
                        >
                            <td class="px-4 py-2 font-medium">
                                {{ container.name }}
                            </td>
                            <!-- <td class="px-4 py-2">{{ container.image }}</td> -->
                            <td class="px-4 py-2">{{ container.version }}</td>
                            <td class="px-4 py-2">{{ container.uptime }}</td>
                            <td class="px-4 py-2">
                                <span
                                    :class="statusBadgeClass(container.status)"
                                >
                                    {{ container.status }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </CardContent>
    </Card>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

defineProps({
    containers: {
        type: Array,
        required: true,
    },
})

function statusBadgeClass(status) {
    const base = 'px-2 py-1 rounded text-xs text-white'
    switch (status) {
        case 'Läuft':
            return `${base} bg-green-500`
        case 'Beendet':
            return `${base} bg-gray-500`
        case 'Fehler':
            return `${base} bg-red-500`
        default:
            return `${base} bg-neutral-500`
    }
}
</script>
