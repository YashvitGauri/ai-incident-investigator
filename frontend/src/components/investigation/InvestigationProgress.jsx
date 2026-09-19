import { useEffect, useState } from 'react'

const phases = [
  {
    title: 'Preparing investigation',
    description: 'Validating and preparing the submitted log data.',
  },
  {
    title: 'Parsing security events',
    description: 'Converting raw log entries into structured events.',
  },
  {
    title: 'Correlating suspicious activity',
    description: 'Analyzing findings and identifying related activity.',
  },
  {
    title: 'Running AI investigation',
    description: 'The investigation agent is analyzing the available evidence.',
  },
  {
    title: 'Building investigation report',
    description: 'Preparing the final structured investigation results.',
  },
]

function InvestigationProgress({ active }) {
  const [phaseIndex, setPhaseIndex] = useState(0)

  useEffect(() => {
    if (!active) {
      setPhaseIndex(0)
      return
    }

    const interval = setInterval(() => {
      setPhaseIndex((current) =>
        current < phases.length - 1 ? current + 1 : current
      )
    }, 1800)

    return () => clearInterval(interval)
  }, [active])

  if (!active) {
    return null
  }

  return (
    <div className="mt-6 overflow-hidden rounded-xl border border-[#263a54] bg-[#0d1420]">
      <div className="border-b border-[#1d2a3a] px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-blue-400/20 bg-blue-400/10">
            <span className="h-2 w-2 animate-pulse rounded-full bg-blue-400" />
          </div>

          <div>
            <p className="text-[13px] font-semibold text-slate-200">
              Investigation in progress
            </p>

            <p className="mt-0.5 text-[11px] text-slate-600">
              Analyzing submitted security events
            </p>
          </div>
        </div>
      </div>

      <div className="px-6 py-6">
        <div className="space-y-5">
          {phases.map((phase, index) => {
            const completed = index < phaseIndex
            const current = index === phaseIndex

            return (
              <div
                key={phase.title}
                className="flex items-start gap-4"
              >
                <div
                  className={`
                    mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border
                    ${
                      completed
                        ? 'border-emerald-400/30 bg-emerald-400/10'
                        : current
                          ? 'border-blue-400/30 bg-blue-400/10'
                          : 'border-[#263445] bg-[#0a111a]'
                    }
                  `}
                >
                  {completed ? (
                    <span className="text-[10px] text-emerald-400">
                      ✓
                    </span>
                  ) : current ? (
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-blue-400" />
                  ) : null}
                </div>

                <div className="min-w-0">
                  <p
                    className={`text-[13px] font-medium ${
                      completed || current
                        ? 'text-slate-200'
                        : 'text-slate-600'
                    }`}
                  >
                    {phase.title}
                  </p>

                  {current && (
                    <p className="mt-1 text-[11px] leading-5 text-slate-500">
                      {phase.description}
                    </p>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <div className="mt-7 border-t border-[#172334] pt-4">
          <p className="text-[10px] text-slate-600">
            Investigation tools are read-only. Your submitted events are not modified.
          </p>
        </div>
      </div>
    </div>
  )
}

export default InvestigationProgress