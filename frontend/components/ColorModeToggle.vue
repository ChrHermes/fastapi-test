<template>
    <Button variant="ghost" @click="toggle" class="text-xl">
      <span class="material-icons">
        {{ icon }}
      </span>
    </Button>
  </template>
  
  <script setup>
  const colorMode = useColorMode()
  
  function toggle() {
    colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'
  }
  
  const icon = computed(() =>
    colorMode.value === 'dark' ? 'light_mode' : 'dark_mode'
  )
  </script>
  