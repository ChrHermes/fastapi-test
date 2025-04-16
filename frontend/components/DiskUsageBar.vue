<template>
    <div class="mt-6">
      <p class="text-sm text-muted-foreground mb-1">{{ label }}</p>
  
      <div class="w-full bg-muted h-3 rounded overflow-hidden">
        <div
          class="h-3 rounded"
          :class="sdBarColor(percent)"
          :style="{ width: percent + '%' }"
        />
      </div>
  
      <p class="text-xs text-muted-foreground mt-1">
        {{ used }} von {{ total }} verwendet ({{ percent }}%)
      </p>
    </div>
  </template>
  
  <script setup>
  import { sdBarColor } from '@/utils/statusColors'
  
  const props = defineProps({
    label: String,
    used: String,
    total: String,
    percent: Number
  })
  </script>
  