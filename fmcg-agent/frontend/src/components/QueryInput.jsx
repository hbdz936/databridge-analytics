import { useState } from 'react'

export default function QueryInput({ onSubmit, loading }) {
  const [value, setValue] = useState('')

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey && value.trim()) {
      e.preventDefault()
      onSubmit(value.trim())
      setValue('')
    }
  }

  return (
    <div style={{
      border: `1px solid ${loading ? 'var(--amber-dim)' : 'var(--border-bright)'}`,
      background: 'var(--bg-card)',
      transition: 'border-color 0.2s'
    }}>
      <div style={{
        padding: '6px 14px',
        borderBottom: `1px solid var(--border)`,
        fontSize: 10, color: 'var(--text-dim)',
        letterSpacing: '0.15em',
        display: 'flex', justifyContent: 'space-between'
      }}>
        <span>QUERY INPUT</span>
        <span style={{ color: loading ? 'var(--amber)' : 'var(--text-dim)' }}>
          {loading ? '● PROCESSING' : '○ READY'}
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', padding: '10px 14px', gap: 10 }}>
        <span style={{ color: 'var(--amber)', fontSize: 14 }}>›</span>
        <input
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
          placeholder="Ask a business question about your FMCG data..."
          style={{
            flex: 1, background: 'transparent', border: 'none', outline: 'none',
            color: 'var(--text-primary)', fontFamily: 'var(--mono)',
            fontSize: 13, caretColor: 'var(--amber)'
          }}
        />
        <button
          onClick={() => { if (value.trim()) { onSubmit(value.trim()); setValue('') } }}
          disabled={loading || !value.trim()}
          style={{
            background: 'var(--amber)', border: 'none',
            color: '#0a0a08', padding: '4px 14px',
            fontFamily: 'var(--mono)', fontSize: 11,
            fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer',
            letterSpacing: '0.1em', opacity: loading ? 0.5 : 1
          }}
        >
          RUN
        </button>
      </div>
    </div>
  )
}