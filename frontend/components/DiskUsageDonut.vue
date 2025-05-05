<template>
  <div class="flex flex-col items-center space-y-2 w-full max-w-[10rem] mx-auto">
    <p class="text-sm text-muted-foreground">{{ label }}</p>

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
  disk: {
    type: Object,
    required: true,
    // { label: 'SD-Karte', used: '3.7 GB', total: '8 GB', percent: 46.25 }
  },
})

const label = props.disk.label

const percent = computed(() => Math.round(props.disk.percent))
const usedShort = computed(() => parseFloat(props.disk.used).toFixed(1))
const totalShort = computed(() => parseFloat(props.disk.total).toFixed(1))

function getUsageColor(percent) {
  if (percent < 50) return '#4ade80'   // grün
  if (percent <= 75) return '#facc15'  // gelb
  return '#f43f5e'                     // rot
}

const chartData = computed(() => ({
  labels: ['Verwendet', 'Frei'],
  datasets: [
    {
      data: [percent.value, 100 - percent.value],
      backgroundColor: [getUsageColor(percent.value), '#e5e7eb'], // grau für frei
      borderWidth: 0,
    },
  ],
}))

const chartOptions = {
  cutout: '70%',
  plugins: {
    legend: { display: false },
  },
}
</script>
