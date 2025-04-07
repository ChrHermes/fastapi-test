import { useApi } from './useApi'

export const useData = async () => {
  const api = useApi()

  const [system, network, database, containers, logs] = await Promise.all([
    api('/api/system'),
    api('/api/network'),
    api('/api/database'),
    api('/api/containers'),
    api('/api/logs?limit=50'),
  ])

  return {
    system,
    network,
    database,
    containers,
    logs,
  }
}
