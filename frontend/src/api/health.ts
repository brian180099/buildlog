export type HealthData = {
  status: string
  service: string
  environment: string
  timestamp: string
}

type HealthResponse = {
  data: HealthData
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export async function getHealth(): Promise<HealthData> {
  const response = await fetch(`${apiBaseUrl}/api/health`)

  if (!response.ok) {
    throw new Error('백엔드 상태를 확인할 수 없습니다.')
  }

  const result = (await response.json()) as HealthResponse
  return result.data
}

