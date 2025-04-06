<template>
    <div class="min-h-screen flex flex-col">
        <header
            class="w-full px-6 py-4 border-b flex items-center justify-between bg-background"
        >
            <h1 class="text-xl font-semibold">DemoBox Admin</h1>
            <div class="flex items-center gap-4">
                <RefreshToggleButton :show-label="false" />

                <ColorModeToggle />

                <Button variant="outline" class="text-sm">
                    <span class="material-icons text-base mr-1">logout</span>
                    Logout
                </Button>
            </div>
        </header>

        <main class="flex-1 p-6">
            <slot />
        </main>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import ColorModeToggle from '@/components/ColorModeToggle.vue'
import RefreshToggleButton from '@/components/RefreshToggleButton.vue'
import { ref, provide, onMounted } from 'vue'

const refreshTrigger = ref(0)
const autoRefreshEnabled = ref(false)
const secondsLeft = ref(60)

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
