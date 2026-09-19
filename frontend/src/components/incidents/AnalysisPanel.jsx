function AnalysisPanel({ analysis }) {
  return (
    <div className="rounded-lg border border-[#263a54] bg-[#0b1421] p-5">

      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-blue-400/20 bg-blue-400/10 text-[10px] font-bold tracking-wide text-blue-300">
          AI
        </div>

        <div>
          <p className="text-[13px] font-semibold text-slate-200">
            Investigation analysis
          </p>

          <p className="mt-0.5 text-[11px] text-slate-600">
            AI-assisted interpretation of observed activity
          </p>
        </div>
      </div>

      <div className="mt-5 border-t border-[#1b2b3e] pt-5">
        <p className="text-[14px] leading-7 text-slate-300">
          {analysis}
        </p>
      </div>
    </div>
  )
}

export default AnalysisPanel