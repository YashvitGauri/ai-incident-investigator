function SeverityBadge({ severity }) {
  const styles = {
    High: {
      wrapper: 'border-red-400/20 bg-red-400/10 text-red-300',
      dot: 'bg-red-400',
    },
    Medium: {
      wrapper: 'border-amber-400/20 bg-amber-400/10 text-amber-300',
      dot: 'bg-amber-400',
    },
    Low: {
      wrapper: 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300',
      dot: 'bg-emerald-400',
    },
  }

  const current = styles[severity] ?? {
    wrapper: 'border-slate-400/20 bg-slate-400/10 text-slate-300',
    dot: 'bg-slate-400',
  }

  return (
    <span
      className={`inline-flex items-center gap-2 rounded-md border px-2.5 py-1 text-xs font-semibold tracking-wide ${current.wrapper}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${current.dot}`} />
      {severity}
    </span>
  )
}

export default SeverityBadge