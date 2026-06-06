export default function CriticCard({ feedback }) {
  const lines = feedback?.split('\n').filter(Boolean) || []

  // Extract scores like "5/5"
  const scoreLines = lines.filter(l => l.includes('/5'))
  const overallLine = lines.find(l => l.toLowerCase().includes('overall'))
  const overallScore = overallLine?.match(/(\d)\/5/)?.[1]

  return (
    <div style={{ border: `1px solid var(--border)`, background: 'var(--bg-card)' }}>
      <div style={{
        padding: '6px 14px', borderBottom: `1px solid var(--border)`,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
      }}>
        <span style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em' }}>CRITIC EVALUATION</span>
        {overallScore && (
          <span style={{
            fontSize: 11, fontWeight: 600,
            color: overallScore >= 4 ? 'var(--green-bright)' : 'var(--amber)'
          }}>
            {overallScore}/5
          </span>
        )}
      </div>
      <div style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: 8 }}>
        {scoreLines.map((line, i) => {
          const score = line.match(/(\d)\/5/)?.[1]
          const label = line.replace(/\*\*/g, '').split(':')[0].trim()
          const comment = line.split('—')[1]?.trim() || ''
          const pct = score ? (parseInt(score) / 5) * 100 : 0
          return (
            <div key={i}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 10, color: 'var(--text-secondary)' }}>{label}</span>
                <span style={{ fontSize: 10, color: 'var(--amber)' }}>{score}/5</span>
              </div>
              <div style={{ height: 2, background: 'var(--border)', position: 'relative' }}>
                <div style={{
                  position: 'absolute', left: 0, top: 0, height: '100%',
                  width: `${pct}%`,
                  background: pct >= 80 ? 'var(--green)' : 'var(--amber-dim)',
                  transition: 'width 0.4s ease'
                }} />
              </div>
              {comment && (
                <div style={{ fontSize: 10, color: 'var(--text-dim)', marginTop: 3 }}>
                  {comment.slice(0, 80)}{comment.length > 80 ? '...' : ''}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}