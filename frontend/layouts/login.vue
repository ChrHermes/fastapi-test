<template>
    <div class="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
      <!-- Theme Toggle oben rechts -->
      <div class="absolute top-4 right-4 z-20">
        <ColorModeToggle />
      </div>
  
      <!-- Schwebendes Logo mittig zwischen Rand und Formular -->
      <div class="absolute top-[12%] w-full flex justify-center pointer-events-none z-10">
        <img src="/img/watermark.png" alt="Logo" class="w-1/2 max-w-xs opacity-20 animate-float" />
      </div>
  
      <main class="relative z-20 w-full max-w-md p-6 animate-fadeInUp">
        <slot />
      </main>
    </div>
  </template>
  
  <script setup>
  import ColorModeToggle from '@/components/ColorModeToggle.vue'
  </script>
  