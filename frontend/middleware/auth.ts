// middleware/auth.ts

export default defineNuxtRouteMiddleware(async () => {
  const { checkAuth } = useAuth()

  const valid = await checkAuth()
  if (!valid) return navigateTo('/login')
})
