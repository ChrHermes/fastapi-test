<template>
  <div class="flex items-center gap-2">
    <Button
      :variant="autoRefreshEnabled ? 'default' : 'outline'"
      @click="toggleAutoRefresh"
      :class="buttonClass"
    >
      <span class="material-icons text-base">
        {{ autoRefreshEnabled ? 'autorenew' : 'refresh' }}
      </span>
      <span v-if="showLabel">
        {{ autoRefreshEnabled ? 'Auto-Refresh an' : 'Jetzt aktualisieren' }}
      </span>
    </Button>
    <span
      v-if="autoRefreshEnabled"
      class="text-xs text-muted-foreground tabular-nums min-w-[28px] text-right"
    >
      {{ secondsLeft }}s
    </span>
  </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { inject, computed } from 'vue'

const props = defineProps({
  showLabel: {
    type: Boolean,
    default: true,
  },
})

const refreshTrigger = inject('refreshTrigger')
const autoRefreshEnabled = inject('autoRefreshEnabled')
const toggleAutoRefresh = inject('toggleAutoRefresh')
const secondsLeft = inject('secondsLeft')

const buttonClass = computed(() => {
  return props.showLabel
    ? 'flex items-center gap-2 min-w-[170px] justify-between'
    : 'w-9 h-9 p-0 justify-center'
})
</script>
