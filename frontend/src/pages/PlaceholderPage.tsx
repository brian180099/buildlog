type PlaceholderPageProps = {
  title: string
  phase?: string
}

export function PlaceholderPage({ title, phase }: PlaceholderPageProps) {
  return (
    <section className="page-heading">
      <p className="eyebrow">{phase ?? 'BuildLog'}</p>
      <h1>{title}</h1>
      <p>이 화면은 계획에 따라 다음 개발 단계에서 기능을 연결합니다.</p>
    </section>
  )
}

