<template>
    <InnerCard icon="dns" title="Datenbank">
        <div
            class="grid xl:grid-cols-[1fr_auto] gap-y-2 xl:gap-x-4 items-start"
        >
            <div class="min-w-0 whitespace-nowrap overflow-hidden">
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

            <div class="justify-self-start self-end xl:self-center">
                <SecureConfirmDialog
                    title="Datenbank zurücksetzen?"
                    description="Diese Aktion löscht alle gespeicherten Daten dauerhaft."
                    confirmation-code="reset-db"
                    confirm-variant="destructive"
                    variant="destructive"
                    icon="delete_forever"
                    text="Zurücksetzen"
                    @confirm="$emit('reset-db')"
                    class="w-auto"
                />
            </div>
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

defineEmits(["reset-db"]);

</script>
