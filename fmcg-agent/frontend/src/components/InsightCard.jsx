export default function InsightCard({ insights, query }) {
  const lines = insights?.split('\n').filter(Boolean) || []

  return (
    <div style={{ border: `1px solid var(--border)`, background: 'var(--bg-card)' }}>
      <div style={{
        padding: '6px 14px', borderBottom: `1px solid var(--border)`,
        display: 'flex', justifyContent: 'space-between'
      }}>
        <span style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em' }}>INTELLIGENCE REPORT</span>
        <span style={{ fontSize: 10, color: 'var(--text-dim)' }}>{new Date().toISOString().slice(0, 19).replace('T', ' ')} UTC</span>
      </div>
      <div style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', gap: 10 }}>
        {lines.map((line, i) => {
          const isBold = line.startsWith('**')
          const isBullet = line.startsWith('-')
          const clean = line.replace(/\*\*/g, '').replace(/^- /, '')

          if (isBold && line.toLowerCase().includes('key finding')) {
            return (
              <div key={i} style={{
                borderLeft: `3px solid var(--amber)`,
                paddingLeft: 12,
                color: 'var(--text-primary)',
                fontSize: 13, fontWeight: 500
              }}>
                {clean.replace('Key Finding:', '').trim()}
              </div>
            )
          }
          if (isBold) {
            return (
              <div key={i} style={{
                fontSize: 10, color: 'var(--amber)',
                letterSpacing: '0.12em', marginTop: 8
              }}>
                {clean.toUpperCase()}
              </div>
            )
          }
          if (isBullet) {
            return (
              <div key={i} style={{ display: 'flex', gap: 10, fontSize: 12, color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--amber-dim)', flexShrink: 0 }}>◆</span>
                <span>{clean}</span>
              </div>
            )
          }
          return (
            <div key={i} style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{clean}</div>
          )
        })}
      </div>
    </div>
  )
}