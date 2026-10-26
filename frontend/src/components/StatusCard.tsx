type StatusCardProps = {
  title: string
  description: string
  status: string
  pending?: boolean
}

export function StatusCard({ title, description, status, pending = false }: StatusCardProps) {
  return (
    <article className="status-card">
      <h2>{title}</h2>
      <p>{description}</p>
      <span className={pending ? 'status pending' : 'status'}>{status}</span>
    </article>
  )
}

