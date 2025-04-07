export function loadBadgeClass(value: number): string {
    const base = 'text-white px-2 py-1 rounded text-xs'
    if (value > 2.5) return `${base} bg-red-500`
    if (value > 1.5) return `${base} bg-yellow-500`
    return `${base} bg-green-500`
  }
  
  export function sdBarColor(percent: number): string {
    if (percent > 75) return 'bg-red-500'
    if (percent > 50) return 'bg-yellow-500'
    return 'bg-green-500'
  }
  