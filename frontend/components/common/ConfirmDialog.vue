<template>
    <Dialog>
        <DialogTrigger as-child>
            <Button :variant="variant" :class="buttonClass">
                <template v-if="hasSlot">
                    <slot />
                </template>
                <template v-else>
                    <span v-if="icon" class="material-icons text-base mr-1">{{ icon }}</span>
                    <span>{{ text }}</span>
                </template>
            </Button>
        </DialogTrigger>

        <DialogContent class="max-w-sm">
            <DialogHeader>
                <DialogTitle>{{ title }}</DialogTitle>
                <DialogDescription>{{ description }}</DialogDescription>
            </DialogHeader>

            <slot name="body" />

            <div class="flex justify-end gap-2 mt-4">
                <DialogClose as-child>
                    <Button variant="ghost">Abbrechen</Button>
                </DialogClose>

                <DialogClose as-child>
                    <Button :variant="confirmVariant" :disabled="confirmDisabled" @click="confirm">
                        Bestätigen
                    </Button>
                </DialogClose>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { useSlots, computed } from 'vue'
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

const slots = useSlots()
const emit = defineEmits(['confirm'])

const props = defineProps({
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
    icon: {
        type: String,
        default: '',
    },
    text: {
        type: String,
        default: '',
    },
    confirmDisabled: {
        type: Boolean,
        default: false,
    },
})

function confirm() {
    emit('confirm')
}

const hasSlot = computed(() => !!slots.default)
</script>
