import IncidentCard from './IncidentCard'

function IncidentResults({ investigation }) {
  if (!investigation?.incidents?.length) {
    return (
      <div className="mt-10 rounded-xl border border-[#1d2a3a] bg-[#0d1420] p-7">
        <div className="flex items-center gap-3">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />

          <p className="text-sm font-medium text-slate-300">
            No security incidents detected
          </p>
        </div>

        <p className="mt-2 text-[13px] leading-6 text-slate-600">
          The provided events did not produce any correlated security findings.
        </p>
      </div>
    )
  }

  return (
    <section className="mt-12">

      <div className="mb-5 flex items-end justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />

            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-300/70">
              Investigation results
            </p>
          </div>

          <h2 className="mt-2 text-xl font-semibold tracking-tight text-slate-100">
            {investigation.incidents.length}{' '}
            {investigation.incidents.length === 1
              ? 'incident'
              : 'incidents'}{' '}
            detected
          </h2>
        </div>

        <span className="hidden font-mono text-[10px] tracking-wider text-slate-700 sm:block">
          ANALYSIS COMPLETE
        </span>
      </div>

      <div className="space-y-6">
        {investigation.incidents.map((incident) => (
          <IncidentCard
            key={incident.incident_id}
            incident={incident}
          />
        ))}
      </div>
    </section>
  )
}

export default IncidentResults