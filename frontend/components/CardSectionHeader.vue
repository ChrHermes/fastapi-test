<template>
    <CardHeader class="border-b pb-2 flex items-start justify-between gap-2">
      <!-- Titel + optional Icon/Subtitel -->
      <div class="flex flex-col">
        <div class="flex items-center gap-2">
          <span v-if="icon" class="material-icons text-base text-muted-foreground">{{ icon }}</span>
          <CardTitle class="text-base font-semibold leading-tight">
            <slot />
          </CardTitle>
        </div>
        <p v-if="subtitle" class="text-xs text-muted-foreground mt-0.5">
          {{ subtitle }}
        </p>
      </div>
  
      <!-- Collapse Toggle -->
      <button
        v-if="collapsible"
        @click="toggle"
        class="text-muted-foreground hover:text-foreground transition"
      >
        <span class="material-icons text-base">
          {{ modelValue ? 'expand_more' : 'expand_less' }}
        </span>
      </button>
    </CardHeader>
  </template>
  
  <script setup>
  import { CardHeader, CardTitle } from '@/components/ui/card'
  
  const props = defineProps({
    icon: String,
    subtitle: String,
    collapsible: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  function toggle() {
    emit('update:modelValue', !props.modelValue)
  }
  </script>
  