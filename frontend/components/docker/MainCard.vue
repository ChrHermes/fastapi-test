<template>
  <Card>
    <LayoutCardSectionHeader icon="apps"
      :subtitle="`${containers.length} Container ${containers.length === 1 ? 'läuft' : 'laufen'} aktuell`">
      Docker
    </LayoutCardSectionHeader>

    <CardContent>
      <div class="overflow-auto">
        <table class="w-full text-sm text-left">
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
            <tr v-for="container in containers" :key="container.name" class="border-t">
              <td class="px-4 py-2 font-medium">{{ container.name }}</td>
              <td class="px-4 py-2">{{ container.version }}</td>
              <td class="px-4 py-2">{{ container.uptime }}</td>
              <td class="px-4 py-2">
                <span :class="statusBadgeClass(container.status)">
                  {{ container.status }}
                </span>
              </td>
              <td class="px-4 py-2 text-center">
                <button
                  class="text-muted-foreground hover:text-foreground"
                  @click="showContainerInfo(container)"
                >
                  <span class="material-icons text-sm">info</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </CardContent>
  </Card>

  <DockerInfoModal :open="modalOpen" :container="selectedContainer" @update:open="modalOpen = $event" />

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
