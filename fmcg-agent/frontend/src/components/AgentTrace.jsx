export default function AgentTrace({ steps, sequence }) {
  const statusColor = {
    running: 'var(--amber)',
    done: 'var(--green-bright)',
    error: 'var(--red-bright)',
    pending: 'var(--text-dim)'
  }
  const statusSymbol = { running: '◌', done: '◆', error: '✗', pending: '◇' }

  return (
    <div>
      <div style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em', marginBottom: 12 }}>
        AGENT PIPELINE
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
        {sequence.map((agent, i) => {
          const step = steps.find(s => s.key === agent.key)
          const status = step?.status || 'pending'
          return (
            <div key={agent.key} style={{ display: 'flex', gap: 10, paddingBottom: 10, position: 'relative' }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <span style={{ color: statusColor[status], fontSize: 12, lineHeight: 1 }}>
                  {statusSymbol[status]}
                </span>
                {i < sequence.length - 1 && (
                  <div style={{
                    width: 1, flex: 1, minHeight: 16,
                    background: status === 'done' ? 'var(--green)' : 'var(--border)',
                    margin: '3px 0'
                  }} />
                )}
              </div>
              <div style={{ paddingBottom: 2 }}>
                <div style={{
                  fontSize: 10, fontWeight: 600,
                  color: status === 'pending' ? 'var(--text-dim)' : statusColor[status],
                  letterSpacing: '0.1em'
                }}>
                  {agent.label}
                </div>
                <div style={{ fontSize: 10, color: 'var(--text-dim)' }}>{agent.desc}</div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}