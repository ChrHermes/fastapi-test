<!-- components/LayoutInnerCard.vue -->
<template>
    <Card
        :class="cardClass"
        class="border border-muted shadow-none gap-2 pt-2 pb-2"
        v-bind="$attrs"
    >
        <CardHeader>
            <div class="flex items-center gap-2">
                <span
                    v-if="icon"
                    class="material-icons text-sm text-muted-foreground"
                >
                    {{ icon }}
                </span>
                <CardTitle class="text-sm font-semibold leading-tight">
                    {{ title }}
                </CardTitle>
            </div>
        </CardHeader>

        <CardContent class="space-y-0.5 text-sm">
            <slot />
        </CardContent>
    </Card>
</template>

<script setup lang="ts">
const props = withDefaults(
    defineProps<{
        title: string
        icon?: string
        colSpan?: number
        rowSpan?: number
    }>(),
    {
        icon: '',
        colSpan: 1,
        rowSpan: 1,
    }
)

const cardClass = computed(() => {
    return `col-span-${props.colSpan} row-span-${props.rowSpan}`
})
</script>
