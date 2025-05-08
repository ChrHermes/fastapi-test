<template>
  <CardHeader class="border-b pb-2 flex items-start justify-between gap-2">
    <div class="flex flex-col">
      <div class="flex items-center gap-2">
        <span v-if="icon" class="material-icons text-base text-muted-foreground">{{ icon }}</span>
        <CardTitle class="text-base font-semibold leading-tight">
          <slot />
        </CardTitle>
      </div>
      <p v-if="subtitle" class="text-xs text-muted-foreground mt-0.5">{{ subtitle }}</p>
    </div>
  </CardHeader>
</template>

<script setup>
import { CardHeader, CardTitle } from '@/components/ui/card'

defineProps({
  icon: String,
  subtitle: String,
})
</script>
