import { useState } from 'react'

export default function SqlViewer({ sql, validation, rowCount }) {
  const [copied, setCopied] = useState(false)

  function copy() {
    navigator.clipboard.writeText(sql)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const validationColor = validation === 'success' ? 'var(--green-bright)'
    : validation === 'fixed' ? 'var(--amber)' : 'var(--red-bright)'

  return (
    <div style={{ border: `1px solid var(--border)`, background: 'var(--bg-card)' }}>
      <div style={{
        padding: '6px 14px', borderBottom: `1px solid var(--border)`,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
      }}>
        <span style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em' }}>GENERATED SQL</span>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <span style={{ fontSize: 10, color: validationColor }}>
            ● {validation?.toUpperCase()}
          </span>
          <button onClick={copy} style={{
            background: 'none', border: 'none', cursor: 'pointer',
            color: copied ? 'var(--green-bright)' : 'var(--text-dim)',
            fontSize: 10, fontFamily: 'var(--mono)'
          }}>
            {copied ? 'COPIED' : 'COPY'}
          </button>
        </div>
      </div>
      <pre style={{
        padding: '14px', margin: 0, overflowX: 'auto',
        fontSize: 11, color: 'var(--amber-bright)',
        lineHeight: 1.7, whiteSpace: 'pre-wrap', wordBreak: 'break-all'
      }}>
        {sql}
      </pre>
      <div style={{
        padding: '6px 14px', borderTop: `1px solid var(--border)`,
        fontSize: 10, color: 'var(--text-dim)'
      }}>
        {rowCount} rows returned
      </div>
    </div>
  )
}