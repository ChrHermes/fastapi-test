<!-- components/InnerCard.vue -->
<template>
    <Card class="border border-muted shadow-none gap-4 pt-2 pb-2 " v-bind="$attrs">
        <CardHeader class="">
            <div class="flex items-center gap-2">
          <span
            v-if="icon"
            class="material-icons text-base text-muted-foreground"
          >
            {{ icon }}
          </span>
          <CardTitle class="text-base font-semibold leading-tight">
            {{ title }}
          </CardTitle>
        </div>
      </CardHeader>
      
      <CardContent class="space-y-0.5 text-sm">
        <slot />
      </CardContent>
    </Card>
  </template>
  
  <script setup lang="ts">
  withDefaults(
    defineProps<{
      title: string
      icon?: string
    }>(),
    {
      icon: '',
    }
  )
  </script>
  