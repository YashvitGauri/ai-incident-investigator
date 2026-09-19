function Header() {
  return (
    <header className="flex h-[72px] items-center justify-between border-b border-[#172334] bg-[#080d15]/95 px-8">
      <div>
        <p className="text-[14px] font-semibold text-slate-200">
          Investigation
        </p>

        <p className="mt-0.5 text-[11px] text-slate-600">
          Analyze security events and investigate incidents
        </p>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-md border border-[#1d2a3a] bg-[#0d1420] px-3 py-2">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />

          <span className="text-[11px] font-medium text-slate-400">
            API Connected
          </span>
        </div>
      </div>
    </header>
  )
}

export default Header