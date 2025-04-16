<template>
  <div class="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
    <!-- Schwebendes Logo -->
    <div class="absolute top-[12%] w-full flex justify-center pointer-events-none z-10">
      <img src="/img/watermark.png" alt="Logo" class="w-1/2 max-w-xs opacity-20 animate-float" />
    </div>

    <!-- Fehlerinhalt -->
    <main class="relative z-20 w-full max-w-md p-8 animate-fadeInUp text-center space-y-6 border rounded-xl bg-card shadow-lg">
      <!-- Icon + Headline -->
      <div class="flex flex-col items-center gap-2">
        <span class="material-icons text-red-500 text-5xl">error_outline</span>
        <h1 class="text-xl font-stretch-75% text-red-500">Es ist ein Fehler aufgetreten</h1>
      </div>

      <!-- Fehlercode -->
      <div v-if="error?.statusCode" class="text-foreground text-8xl font-bold drop-shadow tracking-wider">
        {{ error.statusCode }}
      </div>

      <!-- Nachricht -->
      <p class="text-muted-foreground text-base leading-relaxed">
        {{ error?.message || 'Etwas ist schiefgelaufen. Bitte versuche es später erneut.' }}
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
function handleError() {
  clearError({ redirect: '/' })
}
</script>
