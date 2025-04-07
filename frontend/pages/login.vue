<template>
  <div class="z-10 w-full max-w-md p-8 rounded-2xl shadow-lg border bg-card space-y-6">
    <h1 class="text-2xl font-semibold text-center">Anmeldung</h1>
    <form class="space-y-4" @submit.prevent="onLogin">
      <div>
        <label for="username" class="block text-sm font-medium text-muted-foreground">Benutzername</label>
        <Input id="username" v-model="username" placeholder="admin" class="mt-1 w-full" />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-muted-foreground">Passwort</label>
        <Input id="password" type="password" v-model="password" placeholder="••••••••" class="mt-1 w-full" />
      </div>
      <Button type="submit" class="w-full mt-4">Login</Button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()
const { login } = useAuth()

definePageMeta({
  layout: 'login',
})

function onLogin() {
  const success = login(username.value, password.value)
  if (success) {
    router.push('/')
  } else {
    alert('Ungültige Zugangsdaten')
  }
}
</script>
