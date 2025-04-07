<template>
    <Popover>
      <PopoverTrigger as-child>
        <button
          type="button"
          class="text-[10px] text-muted-foreground hover:text-foreground transition cursor-pointer"
        >
          <span class="material-icons">{{ icon }}</span>
        </button>
      </PopoverTrigger>
      <PopoverContent class="max-w-xs text-xs leading-relaxed">
        <slot v-if="$slots.default" />
        <div v-else v-html="message" />
      </PopoverContent>
    </Popover>
  </template>
  
  <script setup>
  import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover'
  
  defineProps({
    message: {
      type: String,
      default: 'Weitere Informationen verfügbar.',
    },
    icon: {
      type: String,
      default: 'info',
    },
  })
  </script>
  