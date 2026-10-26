import { useEffect, useState } from 'react'
import { getHealth } from '../api/health'
import { StatusCard } from '../components/StatusCard'

type ApiState = 'checking' | 'online' | 'offline'

export function FoundationPage() {
  const [apiState, setApiState] = useState<ApiState>('checking')

  useEffect(() => {
    getHealth()
      .then(() => setApiState('online'))
      .catch(() => setApiState('offline'))
  }, [])

  const apiStatus =
    apiState === 'checking'
      ? '확인 중'
      : apiState === 'online'
        ? '연결됨'
        : '서버 실행 필요'

  return (
    <>
      <section className="page-heading">
        <p className="eyebrow">Phase 1 · Foundation</p>
        <h1>기록을 쌓기 위한 기반이 준비됐어요.</h1>
        <p>
          React 화면과 FastAPI 서버, SQLite3 테스트 데이터베이스와 Supabase 연결 구조를
          먼저 만들었습니다. 실제 기록 기능은 다음 Phase부터 차례로 연결합니다.
        </p>
      </section>

      <section className="status-grid" aria-label="개발 기반 상태">
        <StatusCard
          title="React"
          description="TypeScript와 Vite를 사용하는 프론트엔드입니다."
          status="준비 완료"
        />
        <StatusCard
          title="FastAPI"
          description="화면 요청과 데이터 처리를 담당하는 API 서버입니다."
          status={apiStatus}
          pending={apiState !== 'online'}
        />
        <StatusCard
          title="Database"
          description="테스트는 SQLite3, 실제 서비스는 Supabase PostgreSQL을 사용합니다."
          status="구조 준비 완료"
        />
      </section>
    </>
  )
}

