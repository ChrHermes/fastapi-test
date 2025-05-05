<template>
  <div class="flex flex-col items-center space-y-2 w-full max-w-[10rem] mx-auto">
    <p class="text-sm text-muted-foreground">Arbeitsspeicher</p>

    <div class="relative w-24 h-24 sm:w-28 sm:h-28">
      <Doughnut :data="chartData" :options="chartOptions" class="w-full h-full" />

      <!-- Zentrum: Prozent + Verbrauch -->
      <div class="absolute inset-0 flex flex-col items-center justify-center leading-tight text-foreground">
        <span class="text-lg sm:text-xl font-bold">{{ percent }}%</span>
        <span class="text-xs">
          {{ usedShort }} / {{ totalShort }}
        </span>
        <span class="text-[0.65rem] text-muted-foreground">GB</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  memory: {
    type: Object,
    required: true,
  },
})

function formatShortGB(bytes) {
  return (bytes / 1024 / 1024 / 1024).toFixed(1)
}

const used = computed(() => props.memory.total - props.memory.available)
const percent = computed(() =>
  props.memory.total > 0 ? Math.round((used.value / props.memory.total) * 100) : 0
)
const usedShort = computed(() => formatShortGB(used.value))
const totalShort = computed(() => formatShortGB(props.memory.total))

const chartData = computed(() => ({
  labels: ['Verwendet', 'Frei'],
  datasets: [
    {
      data: [used.value, props.memory.available],
      backgroundColor: ['#57A0E5', '#e5e7eb'],
      borderWidth: 2,
    },
  ],
}))

const chartOptions = {
  cutout: '65%',
  plugins: {
    legend: { display: false },
  },
}
</script>
