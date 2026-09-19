function InvestigationButton({ onClick, loading, disabled }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || loading}
      className="
        inline-flex
        items-center
        gap-2
        rounded-lg
        border
        border-blue-300/20
        bg-blue-400
        px-4
        py-2.5
        text-[13px]
        font-semibold
        text-[#07101c]
        shadow-[0_4px_20px_rgba(110,168,254,0.12)]
        transition
        hover:bg-blue-300
        disabled:cursor-not-allowed
        disabled:opacity-40
      "
    >
      {loading ? (
        <>
          <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-slate-400 border-t-slate-950" />
          Investigating...
        </>
      ) : (
        <>
          Run Investigation
          <span className="text-base">→</span>
        </>
      )}
    </button>
  )
}

export default InvestigationButton