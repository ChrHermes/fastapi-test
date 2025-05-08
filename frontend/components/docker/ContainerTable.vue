<template>
    <div class="overflow-auto">
        <table
            class="w-full text-sm text-left border-separate border-spacing-y-1"
        >
            <thead class="text-muted-foreground">
                <tr>
                    <th class="px-4 py-2">Name</th>
                    <th class="px-4 py-2">Version</th>
                    <th class="px-4 py-2">Uptime</th>
                    <th class="px-4 py-2">Status</th>
                    <th class="px-4 py-2 text-center">Details</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="container in containers"
                    :key="container.name"
                    class="border-t hover:bg-muted transition-colors duration-200"
                >
                    <td class="px-4 py-2 font-medium text-foreground">
                        {{ container.name }}
                    </td>
                    <td class="px-4 py-2">{{ container.version }}</td>
                    <td class="px-4 py-2">{{ container.uptime }}</td>
                    <td class="px-4 py-2">
                        <DockerStatusBadge
                            :status="container.status"
                        />
                    </td>
                    <td class="px-4 py-2 text-center">
                        <button
                            class="text-muted-foreground hover:text-primary transition-colors"
                            @click="$emit('info', container)"
                            title="Details anzeigen"
                        >
                            <span class="material-icons text-sm">info</span>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
defineProps({
    containers: {
        type: Array,
        required: true,
    },
})
</script>
