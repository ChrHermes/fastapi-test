// composables/useAuth.ts

import { computed } from 'vue'

export const useAuth = () => {
  const user = useState<string | null>('auth_user', () => null)
  const isAuthenticated = computed(() => !!user.value)

  async function login(username: string, password: string) {
    try {
      const res = await $fetch('/api/login', {
        method: 'POST',
        body: { username, password },
        credentials: 'include' // wichtig für Cookies
      })
      user.value = res.username ?? username
      return true
    } catch (e) {
      user.value = null
      return false
    }
  }

  async function checkAuth() {
    if (user.value) return true
    try {
      const res = await $fetch('/api/me', {
        credentials: 'include',
      })
      user.value = res.username
      return true
    } catch {
      user.value = null
      return false
    }
  }

  async function logout() {
    await $fetch('/api/logout', { credentials: 'include' })
    console.log('Logout aufgerufen')
    user.value = null
    await navigateTo('/login', { replace: true })
    location.reload()
  }

  return {
    user,
    login,
    logout,
    checkAuth,
    isAuthenticated,
  }
}
