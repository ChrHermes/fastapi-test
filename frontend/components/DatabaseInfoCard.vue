<template>
    <Card>
        <CardSectionHeader icon="storage">Datenbank</CardSectionHeader>

        <CardContent>
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm">
                        Größe:
                        <strong>{{ database.size.toFixed(2) }} MB</strong>
                    </p>
                    <p class="text-sm text-muted-foreground">
                        Erstellt am: {{ database.created }}
                    </p>
                    <p class="text-sm text-muted-foreground">
                        Zuletzt verändert: {{ database.updated }}
                    </p>
                </div>
                <SecureConfirmDialog
                    title="Datenbank zurücksetzen?"
                    description="Diese Aktion löscht alle gespeicherten Daten dauerhaft."
                    confirmation-code="reset-db"
                    confirm-variant="destructive" variant="destructive" 
                    @confirm="$emit('reset')"
                >
                    <span class="material-icons text-base mr-1"
                        >delete_forever</span
                    >
                    Zurücksetzen
                </SecureConfirmDialog>
            </div>
        </CardContent>
    </Card>
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
