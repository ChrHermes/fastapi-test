// composables/useApi.ts
export const useApi = () => {
    const config = useRuntimeConfig()
    const baseUrl = config.public.apiBase || 'http://localhost:8000' // Default zur lokalen FastAPI
  
    const $fetchApi = $fetch.create({
      baseURL: baseUrl,
      credentials: 'include',
    })
  
    return $fetchApi
  }
  