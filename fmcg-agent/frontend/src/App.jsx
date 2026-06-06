import { useState } from 'react'
import QueryInput from './components/QueryInput'
import AgentTrace from './components/AgentTrace'
import InsightCard from './components/InsightCard'
import SqlViewer from './components/SqlViewer'
import CriticCard from './components/CriticCard'

const SAMPLE_QUESTIONS = [
  'What are the top 5 products by revenue?',
  'Which market has the highest sold quantity?',
  'Show monthly sales trend for Nutrition division',
  'Which customers are in Brick & Mortar channel?',
  'Compare revenue between Sports and Nutrition categories'
]

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [activeQuestion, setActiveQuestion] = useState('')
  const [agentSteps, setAgentSteps] = useState([])

  const AGENT_SEQUENCE = [
    { key: 'orchestrator', label: 'ORCHESTRATOR', desc: 'Refining query intent' },
    { key: 'schema',       label: 'SCHEMA',       desc: 'Mapping table structure' },
    { key: 'sql',          label: 'SQL GEN',      desc: 'Generating Spark SQL' },
    { key: 'validator',    label: 'VALIDATOR',    desc: 'Executing against Databricks' },
    { key: 'insight',      label: 'INSIGHT',      desc: 'Synthesizing business signals' },
    { key: 'critic',       label: 'CRITIC',       desc: 'Evaluating output quality' },
  ]

  async function handleQuery(question) {
    setLoading(true)
    setError(null)
    setResult(null)
    setActiveQuestion(question)
    setAgentSteps([])

    // Simulate agent step progression
    for (let i = 0; i < AGENT_SEQUENCE.length; i++) {
      await new Promise(r => setTimeout(r, 600 * i))
      setAgentSteps(prev => [...prev, { ...AGENT_SEQUENCE[i], status: 'running' }])
    }

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Query failed')

      setAgentSteps(AGENT_SEQUENCE.map(a => ({ ...a, status: 'done' })))
      setResult(data)
    } catch (e) {
      setError(e.message)
      setAgentSteps(prev => prev.map((s, i) =>
        i === prev.length - 1 ? { ...s, status: 'error' } : { ...s, status: 'done' }
      ))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>

      {/* Header */}
      <header style={{
        borderBottom: `1px solid var(--border)`,
        padding: '12px 32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--bg-panel)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{
            width: 8, height: 8, borderRadius: '50%',
            background: 'var(--amber)', boxShadow: '0 0 6px var(--amber)'
          }} />
          <span style={{ color: 'var(--amber)', fontWeight: 600, letterSpacing: '0.12em', fontSize: 12 }}>
            FMCG // ANALYTICS TERMINAL
          </span>
          <span style={{ color: 'var(--text-dim)', fontSize: 11 }}>v1.0 · 6-AGENT PIPELINE</span>
        </div>
        <div style={{ display: 'flex', gap: 20, fontSize: 11, color: 'var(--text-dim)' }}>
          <span>DATABRICKS <span style={{ color: 'var(--green-bright)' }}>◆ LIVE</span></span>
          <span>GROQ LLaMA-3.1</span>
          <span>LangGraph</span>
        </div>
      </header>

      <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '280px 1fr', minHeight: 0 }}>

        {/* Left Sidebar */}
        <aside style={{
          borderRight: `1px solid var(--border)`,
          padding: '24px 20px',
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
          background: 'var(--bg-panel)',
          overflowY: 'auto'
        }}>
          <div>
            <div style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.15em', marginBottom: 12 }}>
              SAMPLE QUERIES
            </div>
            {SAMPLE_QUESTIONS.map((q, i) => (
              <button key={i} onClick={() => handleQuery(q)} disabled={loading}
                style={{
                  display: 'block', width: '100%', textAlign: 'left',
                  background: activeQuestion === q ? 'var(--amber-glow)' : 'transparent',
                  border: 'none',
                  borderLeft: `2px solid ${activeQuestion === q ? 'var(--amber)' : 'var(--border)'}`,
                  color: activeQuestion === q ? 'var(--amber-bright)' : 'var(--text-secondary)',
                  padding: '8px 12px', marginBottom: 4,
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontSize: 11, lineHeight: 1.5,
                  transition: 'all 0.15s',
                  fontFamily: 'var(--mono)'
                }}
              >
                {q}
              </button>
            ))}
          </div>

          {/* Agent Trace in sidebar */}
          {agentSteps.length > 0 && (
            <AgentTrace steps={agentSteps} sequence={AGENT_SEQUENCE} />
          )}
        </aside>

        {/* Main Content */}
        <main style={{ overflowY: 'auto', padding: '28px 32px', display: 'flex', flexDirection: 'column', gap: 20 }}>

          <QueryInput onSubmit={handleQuery} loading={loading} />

          {error && (
            <div style={{
              border: `1px solid var(--red)`,
              background: 'rgba(140,63,63,0.08)',
              padding: '12px 16px', fontSize: 12,
              color: 'var(--red-bright)',
              fontFamily: 'var(--mono)'
            }}>
              ✗ ERROR · {error}
            </div>
          )}

          {loading && !result && (
            <div style={{ color: 'var(--text-dim)', fontSize: 12, padding: '20px 0' }}>
              <span style={{ color: 'var(--amber)' }}>▶</span> Pipeline executing
              <span style={{ animation: 'none' }}>...</span>
            </div>
          )}

          {result && (
            <>
              {/* Refined query banner */}
              <div style={{
                borderLeft: `3px solid var(--amber-dim)`,
                paddingLeft: 14,
                color: 'var(--text-secondary)',
                fontSize: 12
              }}>
                <div style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.12em', marginBottom: 4 }}>
                  REFINED QUERY
                </div>
                {result.refined_query}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <SqlViewer sql={result.generated_sql} validation={result.validation_result} rowCount={result.row_count} />
                <CriticCard feedback={result.critic_feedback} />
              </div>

              <InsightCard insights={result.insights} query={result.user_query} />
            </>
          )}
        </main>
      </div>
    </div>
  )
}