<template>
  <div class="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
    <!-- Schwebendes Logo -->
    <div class="absolute top-[12%] w-full flex justify-center pointer-events-none z-10">
      <img src="/img/watermark.png" alt="Logo" class="w-1/2 max-w-xs opacity-20 animate-float" />
    </div>

    <!-- Fehlerinhalt -->
    <main class="relative z-20 w-full max-w-md p-8 text-center space-y-6 border rounded-xl bg-card shadow-lg">
      <!-- Icon + Headline -->
      <div class="flex flex-col items-center gap-2">
        <span class="material-icons text-red-500 text-5xl">
          {{ icon }}
        </span>
        <h1 class="text-xl font-light text-red-500">
          {{ title }}
        </h1>
      </div>

      <!-- Fehlercode -->
      <div
        v-if="error?.statusCode"
        class="text-foreground text-8xl font-bold drop-shadow tracking-wider"
      >
        {{ error.statusCode }}
      </div>

      <!-- Nachricht -->
      <p class="text-muted-foreground text-base leading-relaxed">
        {{ message }}
      </p>

      <!-- Zurück-Button -->
      <Button @click="handleError" class="mt-2">
        Zurück zur Startseite
      </Button>
    </main>
  </div>
</template>

<script setup>
import { useError } from '#app'
import { Button } from '@/components/ui/button'

const error = useError()

const status = error?.value?.statusCode
const path = error?.value?.url ?? ''

const title = computed(() => {
  if (status === 404) return 'Seite nicht gefunden'
  if (status >= 500) return 'Serverfehler'
  return 'Es ist ein Fehler aufgetreten'
})

const message = computed(() => {
  if (status === 404) return `Die Seite ${path} existiert nicht oder wurde verschoben.`
  if (status >= 500) return 'Der Server hat ein Problem. Bitte versuche es später erneut.'
  return error?.value?.message || 'Ein unerwarteter Fehler ist aufgetreten.'
})

const icon = computed(() => {
  if (status === 404) return 'search_off'
  if (status >= 500) return 'dns'
  return 'error_outline'
})

function handleError() {
  clearError({ redirect: '/' })
}
</script>
