function EvidenceList({ evidence }) {
  if (!evidence?.length) {
    return (
      <p className="text-sm text-slate-500">
        No evidence was returned for this incident.
      </p>
    )
  }

  return (
    <div className="space-y-2">
      {evidence.map((item, index) => {
        const parts = item.split(', ')
        const timestamp = parts[0] ?? ''
        const description = parts.slice(1).join(', ')

        return (
          <div
            key={index}
            className="grid grid-cols-[190px_1fr] gap-5 rounded-lg border border-[#1a2737] bg-[#090f18] px-4 py-4 transition hover:border-[#2a3c52] hover:bg-[#0b131e]"
          >
            <div className="flex items-start gap-3">
              <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-blue-400/80" />

              <div>
                <p className="font-mono text-[11px] leading-5 text-slate-400">
                  {timestamp}
                </p>

                <p className="mt-0.5 text-[9px] font-semibold tracking-[0.12em] text-slate-700">
                  EVENT {String(index + 1).padStart(2, '0')}
                </p>
              </div>
            </div>

            <p className="text-[13px] leading-6 text-slate-300">
              {description}
            </p>
          </div>
        )
      })}
    </div>
  )
}

export default EvidenceList