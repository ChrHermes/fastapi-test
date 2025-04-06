<template>
    <Dialog>
        <DialogTrigger as-child>
            <Button :variant="variant" :class="buttonClass">
                <slot />
            </Button>
        </DialogTrigger>

        <DialogContent class="max-w-sm">
            <DialogHeader>
                <DialogTitle>{{ title }}</DialogTitle>
                <DialogDescription>{{ description }}</DialogDescription>
            </DialogHeader>

            <div class="my-4 space-y-2">
                <p class="text-sm text-muted-foreground">
                    Bitte gib
                    <code class="px-1 py-0.5 bg-muted rounded text-xs">{{
                        confirmationCode
                    }}</code>
                    ein, um fortzufahren.
                </p>
                <Input
                    v-model="input"
                    placeholder="Bestätigungscode eingeben"
                />
            </div>

            <div class="flex justify-end gap-2">
                <DialogClose as-child>
                    <Button variant="ghost">Abbrechen</Button>
                </DialogClose>

                <DialogClose as-child>
                    <Button
                        :variant="confirmVariant"
                        :disabled="input !== confirmationCode"
                        @click="confirm"
                    >
                        Bestätigen
                    </Button>
                </DialogClose>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogClose,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const input = ref('')

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
})

const emit = defineEmits(['confirm'])

function confirm() {
    emit('confirm')
    input.value = ''
}
</script>
