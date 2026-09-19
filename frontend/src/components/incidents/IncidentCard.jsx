import SeverityBadge from './SeverityBadge'
import EvidenceList from './EvidenceList'
import AnalysisPanel from './AnalysisPanel'

function IncidentCard({ incident }) {
  const evidenceCount = incident.observed_evidence?.length ?? 0
  const explanationCount = incident.possible_explanations?.length ?? 0
  const recommendationCount = incident.recommended_actions?.length ?? 0

  return (
    <article className="overflow-hidden rounded-xl border border-[#233246] bg-[#0d1420] shadow-[0_20px_60px_rgba(0,0,0,0.16)]">

      {/* Incident header */}
      <div className="border-b border-[#1d2a3a] px-7 py-6">

        <div className="flex items-start justify-between gap-6">

          <div>
            <div className="flex items-center gap-3">
              <span className="font-mono text-[11px] font-medium text-blue-300">
                {incident.incident_id}
              </span>

              <span className="h-1 w-1 rounded-full bg-slate-700" />

              <span className="text-[11px] text-slate-600">
                Security incident
              </span>
            </div>

            <h2 className="mt-3 text-[22px] font-semibold tracking-[-0.02em] text-slate-100">
              Suspicious authentication activity
            </h2>
          </div>

          <SeverityBadge severity={incident.severity} />
        </div>

        {/* Stats */}
        <div className="mt-7 grid grid-cols-3 overflow-hidden rounded-lg border border-[#1d2a3a] bg-[#090f18]">

          <div className="border-r border-[#1d2a3a] px-5 py-4">
            <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-600">
              Evidence
            </p>

            <p className="mt-1.5 text-lg font-semibold text-slate-200">
              {evidenceCount}
            </p>
          </div>

          <div className="border-r border-[#1d2a3a] px-5 py-4">
            <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-600">
              Explanations
            </p>

            <p className="mt-1.5 text-lg font-semibold text-slate-200">
              {explanationCount}
            </p>
          </div>

          <div className="px-5 py-4">
            <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-600">
              Confidence
            </p>

            <p className="mt-1.5 text-lg font-semibold text-slate-200">
              {incident.confidence}
            </p>
          </div>

        </div>
      </div>

      {/* Summary */}
      <section className="border-b border-[#1d2a3a] px-7 py-7">
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-300/70">
          Incident summary
        </p>

        <p className="mt-3 max-w-4xl text-[14px] leading-7 text-slate-300">
          {incident.summary}
        </p>
      </section>

      {/* Evidence */}
      <section className="border-b border-[#1d2a3a] px-7 py-7">
        <div className="mb-6">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-300/70">
            Observed evidence
          </p>

          <p className="mt-1.5 text-[11px] text-slate-600">
            Events associated with this incident
          </p>
        </div>

        <EvidenceList evidence={incident.observed_evidence} />
      </section>

      {/* AI analysis */}
      <section className="border-b border-[#1d2a3a] px-7 py-7">
        <AnalysisPanel analysis={incident.analysis} />
      </section>

      {/* Explanations + recommendations */}
      <div className="grid gap-px bg-[#1d2a3a] md:grid-cols-2">

        <section className="bg-[#0d1420] px-7 py-7">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-300/70">
            Possible explanations
          </p>

          <ul className="mt-5 space-y-4">
            {incident.possible_explanations?.map((item, index) => (
              <li
                key={index}
                className="flex gap-3 text-[13px] leading-6 text-slate-300"
              >
                <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-slate-600" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="bg-[#0d1420] px-7 py-7">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-300/70">
            Recommended actions
          </p>

          <ul className="mt-5 space-y-4">
            {incident.recommended_actions?.map((item, index) => (
              <li
                key={index}
                className="flex gap-3 text-[13px] leading-6 text-slate-300"
              >
                <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-400" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

      </div>

      {/* Uncertainty */}
      {incident.uncertainty && (
        <div className="border-t border-[#1d2a3a] bg-[#0a111b] px-7 py-5">
          <div className="flex gap-3">
            <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-amber-400/20 bg-amber-400/10 text-[10px] font-bold text-amber-300">
              !
            </div>

            <div>
              <p className="text-[11px] font-semibold text-amber-300">
                Investigation uncertainty
              </p>

              <p className="mt-1.5 text-[13px] leading-6 text-slate-400">
                {incident.uncertainty}
              </p>
            </div>
          </div>
        </div>
      )}

    </article>
  )
}

export default IncidentCard