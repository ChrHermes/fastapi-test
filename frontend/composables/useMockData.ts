// composables/useMockData.ts

import { mockSystem, mockNetwork, mockDatabase, mockContainers, mockLogs } from '@/data/mockData'

export const useMockData = () => {
  const useMock = true

  if (!useMock) {
    // später: API-Integration
    return {
      system: ref(),
      network: ref(),
      database: ref(),
      containers: ref([]),
      logs: ref([]),
    }
  }

  return {
    system: mockSystem,
    network: mockNetwork,
    database: mockDatabase,
    containers: mockContainers,
    logs: mockLogs,
  }
}
