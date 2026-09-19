import { useState } from 'react'
import { investigateLogs } from './services/api'

import Sidebar from './components/layout/Sidebar'
import Header from './components/layout/Header'
import LogInput from './components/investigation/LogInput'
import InvestigationButton from './components/investigation/InvestigationButton'
import InvestigationProgress from './components/investigation/InvestigationProgress'
import IncidentResults from './components/incidents/IncidentResults'


function App() {
  const [logText, setLogText] = useState('')
  const [loading, setLoading] = useState(false)
  const [investigation, setInvestigation] = useState(null)
  const [error, setError] = useState('')

  async function handleInvestigation() {
    if (!logText.trim()) {
      return
    }

    setLoading(true)
    setError('')
    setInvestigation(null)

    try {
      const result = await investigateLogs(logText)
      setInvestigation(result)
    } catch (error) {
      console.error(error)
      setError('Unable to complete the investigation. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-[#080d15] text-slate-200">
      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <Header />

        <main className="flex-1 overflow-auto">
          <div className="mx-auto w-full max-w-[1180px] px-8 py-12">

            {/* Page heading */}
            <div className="max-w-3xl">
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />

                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-blue-300/80">
                  Security Investigation
                </p>
              </div>

              <h1 className="mt-4 text-[38px] font-semibold leading-tight tracking-[-0.03em] text-slate-100">
                Investigate security incidents
              </h1>

              <p className="mt-4 max-w-2xl text-[15px] leading-7 text-slate-400">
                Analyze raw security logs, correlate suspicious activity,
                and use AI-assisted investigation to understand what happened.
              </p>
            </div>

            {/* Input workspace */}
            <div className="mt-10 overflow-hidden rounded-xl border border-[#1d2a3a] bg-[#0d1420] shadow-[0_20px_60px_rgba(0,0,0,0.18)]">

              <div className="border-b border-[#172334] px-6 py-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[13px] font-semibold text-slate-200">
                      Security logs
                    </p>

                    <p className="mt-1 text-[11px] text-slate-600">
                      Paste raw application or security events for analysis
                    </p>
                  </div>

                  <span className="rounded-md border border-[#1d2a3a] bg-[#101925] px-2.5 py-1 text-[10px] font-medium uppercase tracking-wider text-slate-500">
                    Read only
                  </span>
                </div>
              </div>

              <div className="p-6">
                <LogInput
                  value={logText}
                  onChange={setLogText}
                  disabled={loading}
                  onError={setError}
                />

                <div className="mt-5 flex items-center justify-between border-t border-[#172334] pt-5">
                  <span className="text-[11px] text-slate-600">
                    Investigation tools cannot modify your source events.
                  </span>

                  <InvestigationButton
                    onClick={handleInvestigation}
                    loading={loading}
                    disabled={!logText.trim()}
                  />
                </div>
              </div>
            </div>

            <InvestigationProgress active={loading} />
            
            {/* Error */}
            {error && (
              <div className="mt-5 rounded-lg border border-red-400/20 bg-red-400/[0.06] px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* Results */}
            {investigation && (
              <IncidentResults investigation={investigation} />
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App