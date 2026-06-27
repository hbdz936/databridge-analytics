export default function ResultTable({ results }) {
  if (!results || results.length === 0) return null

  const columns = Object.keys(results[0])

  return (
    <div style={{ border: `1px solid var(--border)`, background: 'var(--bg-card)' }}>
      <div style={{
        padding: '6px 14px', borderBottom: `1px solid var(--border)`,
        display: 'flex', justifyContent: 'space-between'
      }}>
        <span style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em' }}>
          RAW RESULTS
        </span>
        <span style={{ fontSize: 10, color: 'var(--text-dim)' }}>
          {results.length} row{results.length !== 1 ? 's' : ''}
        </span>
      </div>
      <div style={{ overflowX: 'auto', maxHeight: 320, overflowY: 'auto' }}>
        <table style={{ width: '100%', fontSize: 11, borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col} style={{
                  textAlign: 'left', padding: '8px 14px',
                  color: 'var(--amber)', borderBottom: `1px solid var(--border)`,
                  whiteSpace: 'nowrap', position: 'sticky', top: 0,
                  background: 'var(--bg-card)'
                }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((row, i) => (
              <tr key={i} style={{ borderBottom: `1px solid var(--border)` }}>
                {columns.map(col => (
                  <td key={col} style={{
                    padding: '6px 14px', color: 'var(--text-secondary)',
                    whiteSpace: 'nowrap'
                  }}>
                    {String(row[col] ?? '—')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}