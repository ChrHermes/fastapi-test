<template>
  <InnerCard icon="save" title="Datenträger">
    <div class="space-y-3 mt-2">
      <div
        v-for="disk in disks"
        :key="disk.label"
        class="space-y-1"
      >
        <template v-if="!disk.error">
          <!-- Label -->
          <p class="text-sm font-medium text-muted-foreground mb-1">
            {{ disk.label }}
          </p>

          <!-- Balken mit getrennten Tooltips -->
          <div class="w-full h-3 rounded overflow-hidden bg-muted flex">
            <!-- Belegter Bereich -->
            <div
              class="h-3"
              :class="sdBarColor(disk.percent)"
              :style="{ width: disk.percent + '%' }"
              :title="`Belegt: ${disk.fmt_used}`"
            ></div>

            <!-- Freier Bereich -->
            <div
              class="h-3 bg-muted-foreground/10"
              :style="{ width: (100 - disk.percent) + '%' }"
              :title="`Frei: ${disk.fmt_free}`"
            ></div>
          </div>

          <!-- Textinfo -->
          <p class="text-xs text-muted-foreground">
            {{ disk.fmt_used }} von {{ disk.fmt_total }} verwendet ({{ disk.percent }} %)
          </p>
        </template>

        <template v-else>
          <p class="text-sm font-medium text-muted-foreground mb-1">
            {{ disk.label }}
          </p>
          <div class="w-full bg-red-100 text-red-600 text-xs px-2 py-1 rounded">
            Fehler beim Zugriff auf {{ disk.mount }}: {{ disk.error }}
          </div>
        </template>
      </div>
    </div>
  </InnerCard>
</template>

<script setup>
import { sdBarColor } from '@/utils/statusColors'

const props = defineProps({
  disks: {
    type: Array,
    required: true,
    // Struktur (Beispiel):
    // {
    //   label: 'Intern',
    //   mount: '/',
    //   byte_used: 1290000000,
    //   byte_free: 39200000000,
    //   byte_total: 40490000000,
    //   fmt_used: '1.29 GB',
    //   fmt_free: '39.20 GB',
    //   fmt_total: '40.49 GB',
    //   percent: 3.19,
    //   error: null | string
    // }
  }
})
</script>
