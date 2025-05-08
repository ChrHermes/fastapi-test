<template>
    <div class="min-h-screen flex flex-col">        
        <Toaster />

        <!-- Ladeoverlay -->
        <div v-if="loading" class="absolute inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary" />
        </div>

        <header class="fixed top-0 left-0 w-full z-50 px-6 py-4 border-b flex items-center justify-between bg-background">
            <h1 class="text-xl font-semibold">DemoBox Admin</h1>
            <div class="flex items-center gap-4">
                <BaseRefreshToggle :show-label="false" v-if="route.path === '/'" />

                <BaseThemeToggle />

                <Button variant="outline" class="text-sm" v-if="user" @click="logout">
                    <span class="material-icons text-base mr-1">logout</span>
                    Logout
                </Button>
            </div>
        </header>

        <main class="flex-1 p-6 pt-20">
            <slot />
        </main>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Button } from '@/components/ui/button'
import { ref, provide, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { Toaster } from '@/components/ui/sonner'

definePageMeta({
  middleware: 'auth', // globaler Auth-Schutz
})

const { user, logout } = useAuth()
const route = useRoute()
const refreshTrigger = ref(0)
const autoRefreshEnabled = ref(false)
const secondsLeft = ref(60)
const loading = ref(false)

function toggleAutoRefresh() {
    if (!autoRefreshEnabled.value) {
        refreshTrigger.value++
        secondsLeft.value = 60
        console.log('Auto-Refresh aktiviert')
    } else {
        console.log('Auto-Refresh deaktiviert')
    }
    autoRefreshEnabled.value = !autoRefreshEnabled.value
}

provide('refreshTrigger', refreshTrigger)
provide('autoRefreshEnabled', autoRefreshEnabled)
provide('toggleAutoRefresh', toggleAutoRefresh)
provide('secondsLeft', secondsLeft)
provide('loading', loading)

onMounted(() => {
    setInterval(() => {
        if (autoRefreshEnabled.value) {
            secondsLeft.value--
            if (secondsLeft.value <= 0) {
                refreshTrigger.value++
                secondsLeft.value = 60
                console.log('Auto-Refresh ausgelöst')
            }
        }
    }, 1000)
})
</script>
