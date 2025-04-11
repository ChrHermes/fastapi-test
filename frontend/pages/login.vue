<template>
  <div class="z-10 w-full max-w-md p-8 rounded-2xl shadow-lg border bg-card space-y-6">
    <h1 class="text-2xl font-semibold text-center">Anmeldung</h1>

    <form class="space-y-4" @submit.prevent="onLogin">
      <div>
        <Input
          id="username"
          v-model="username"
          placeholder="Benutzername"
          class="mt-1 w-full"
        />
      </div>

      <div>
        <Input
          id="password"
          type="password"
          v-model="password"
          placeholder="Passwort"
          class="mt-1 w-full"
        />
      </div>

      <Button type="submit" class="w-full mt-4" :disabled="isSubmitting || !username || !password">
        <span class="material-icons text-base mr-1">login</span>
        Login
      </Button>

      <p v-if="errorMessage" class="text-sm text-red-500 text-center mt-2">
        {{ errorMessage }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'login',
})

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const router = useRouter()
const { login } = useAuth()

async function onLogin() {
  errorMessage.value = ''
  isSubmitting.value = true

  const success = await login(username.value, password.value)

  if (success) {
    router.push('/')
  } else {
    errorMessage.value = 'Benutzername oder Passwort ist falsch.'
  }

  isSubmitting.value = false
}
</script>
