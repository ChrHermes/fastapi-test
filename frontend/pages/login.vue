<template>
    <div class="login-page">
      <!-- Theme-Toggle Button -->
      <button id="theme-toggle" class="theme-toggle" @click="toggleTheme">
        <span class="material-icons" id="theme-icon">{{ themeIcon }}</span>
      </button>
  
      <!-- Login-Form -->
      <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <input
              v-model="username"
              type="text"
              placeholder="Benutzername"
              required
              id="username"
            />
          </div>
  
          <div class="input-group password-group">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Passwort"
              required
              id="password"
            />
            <span class="toggle-password material-icons" @click="togglePassword">
              {{ showPassword ? 'visibility_off' : 'visibility' }}
            </span>
          </div>
  
          <button id="loginButton" type="submit">
            <span class="material-icons icon-button">login</span>Anmelden
          </button>
        </form>
  
        <p v-if="errorMessage" style="color: red; margin-top: 10px;">
          {{ errorMessage }}
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  const username = ref('')
  const password = ref('')
  const showPassword = ref(false)
  const errorMessage = ref('')
  const themeIcon = ref('dark_mode')
  
  function togglePassword() {
    showPassword.value = !showPassword.value
  }
  
  function toggleTheme() {
    const body = document.body
    const isDark = body.classList.toggle('dark-mode')
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
    themeIcon.value = isDark ? 'light_mode' : 'dark_mode'
  }
  
  onMounted(() => {
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode')
      themeIcon.value = 'light_mode'
    } else {
      themeIcon.value = 'dark_mode'
    }
  })
  
  async function handleLogin() {
    if (!username.value || !password.value) {
      errorMessage.value = 'Benutzername und Passwort erforderlich!'
      return
    }
  
    try {
      const response = await $fetch('/login', {
        method: 'POST',
        body: {
          username: username.value,
          password: password.value,
        }
      })
  
      if (response && typeof response === 'object' && response.redirect) {
        return navigateTo(response.redirect)
      }
  
      await navigateTo('/')
    } catch (error) {
      console.error('Fehler beim Login:', error)
      errorMessage.value =
        error?.data?.detail || 'Serverfehler. Bitte später versuchen.'
    }
  }
  </script>
  
  <style scoped>
  .login-page {
    height: 100vh;
  }
  </style>
  