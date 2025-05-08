<template>
    <Card>
        <LayoutCardSectionHeader
            icon="apps"
            :subtitle="`${containers.length} Container ${
                containers.length === 1 ? 'läuft' : 'laufen'
            } aktuell`"
        >
            Docker
        </LayoutCardSectionHeader>

        <CardContent>
            <div class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
                <DockerSingleContainerCard
                    v-for="container in containers"
                    :key="container.name"
                    :container="container"
                    @info="showContainerInfo"
                />
            </div>
            
            <!-- <DockerContainerTable
                :containers="containers"
                @info="showContainerInfo"
            /> -->
        </CardContent>
    </Card>

    <DockerInfoModal
        :open="modalOpen"
        :container="selectedContainer"
        @update:open="modalOpen = $event"
    />
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'

const modalOpen = ref(false)
const selectedContainer = ref(null)

defineProps({
    containers: {
        type: Array,
        required: true,
    },
})

function showContainerInfo(container) {
    selectedContainer.value = container
    modalOpen.value = true
}
</script>
