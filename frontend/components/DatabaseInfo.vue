<template>
    <InnerCard icon="storage" title="Datenbank">
        <div
            class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-2 xl:gap-4"
        >
            <div class="min-w-0 xl:max-w-xl whitespace-nowrap overflow-hidden">
                <p class="text-sm truncate">
                    Größe: <strong>{{ database.size.toFixed(2) }} MB</strong>
                </p>
                <p class="text-sm text-muted-foreground truncate">
                    Erstellt am: {{ database.created }}
                </p>
                <p class="text-sm text-muted-foreground truncate">
                    Zuletzt verändert: {{ database.updated }}
                </p>
            </div>

            <SecureConfirmDialog
                title="Datenbank zurücksetzen?"
                description="Diese Aktion löscht alle gespeicherten Daten dauerhaft."
                confirmation-code="reset-db"
                confirm-variant="destructive"
                variant="destructive"
                icon="delete_forever"
                text="Zurücksetzen"
                @confirm="$emit('reset')"
                class="w-auto self-end xl:self-end xl:ml-4 mt-2 xl:mt-0"
            />
        </div>
    </InnerCard>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'

defineProps({
    database: {
        type: Object,
        required: true,
    },
})
</script>
