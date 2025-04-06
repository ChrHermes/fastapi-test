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
                <DialogDescription>
                    {{ description }}
                </DialogDescription>
            </DialogHeader>

            <div class="flex justify-end gap-2 mt-4">
                <DialogClose as-child>
                    <Button variant="ghost"> Abbrechen </Button>
                </DialogClose>

                <DialogClose as-child>
                    <Button :variant="confirmVariant" @click="confirm">
                        Bestätigen
                    </Button>
                </DialogClose>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
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

defineProps({
    title: String,
    description: String,
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
}
</script>
