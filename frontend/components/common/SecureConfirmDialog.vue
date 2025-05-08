<template>
    <CommonConfirmDialog
        :title="title"
        :description="description"
        :confirm-variant="confirmVariant"
        :variant="variant"
        :button-class="buttonClass"
        :icon="icon"
        :text="text"
        :confirm-disabled="input !== confirmationCode"
        @confirm="handleConfirm"
    >
        <template #body>
            <div class="my-4 space-y-2">
                <p class="text-sm text-muted-foreground">
                    Bitte gib
                    <code class="px-1 py-0.5 bg-muted rounded text-xs">{{ confirmationCode }}</code>
                    ein, um fortzufahren.
                </p>
                <Input v-model="input" placeholder="Bestätigungscode eingeben" />
            </div>
        </template>
    </CommonConfirmDialog>
</template>

<script setup>
import { ref } from 'vue'
import { Input } from '@/components/ui/input'

const props = defineProps({
    title: String,
    description: String,
    confirmationCode: {
        type: String,
        required: true,
    },
    confirmVariant: {
        type: String,
        default: 'destructive',
    },
    variant: {
        type: String,
        default: 'default',
    },
    buttonClass: {
        type: String,
        default: '',
    },
    icon: {
        type: String,
        default: '',
    },
    text: {
        type: String,
        default: '',
    },
})

const emit = defineEmits(['confirm'])

const input = ref('')

function handleConfirm() {
    emit('confirm')
    input.value = ''
}
</script>
