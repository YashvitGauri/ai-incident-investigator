function Sidebar() {
  return (
    <aside className="flex w-[260px] shrink-0 flex-col border-r border-[#172334] bg-[#090e17]">
      {/* Brand */}
      <div className="flex h-[72px] items-center border-b border-[#172334] px-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#2b3c52] bg-[#111b29] text-xs font-bold text-slate-100">
            AI
          </div>

          <div>
            <p className="text-[14px] font-semibold tracking-tight text-slate-100">
              Incident Intel
            </p>

            <p className="mt-0.5 text-[11px] text-slate-500">
              Security Operations
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-7">
        <p className="px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-600">
          Workspace
        </p>

        <div className="mt-3 space-y-1">
          <button className="group flex w-full items-center gap-3 rounded-lg border border-[#24344a] bg-[#121b29] px-3 py-2.5 text-sm font-medium text-slate-100">
            <span className="flex h-5 w-5 items-center justify-center rounded bg-[#1c3554] text-[11px] text-blue-300">
              ↗
            </span>

            Investigate
          </button>

          <button className="group flex w-full items-center gap-3 rounded-lg border border-transparent px-3 py-2.5 text-sm text-slate-500 transition hover:bg-[#101925] hover:text-slate-200">
            <span className="flex h-5 w-5 items-center justify-center text-[12px]">
              ◷
            </span>

            Incidents
          </button>
        </div>
      </nav>

      {/* System status */}
      <div className="border-t border-[#172334] p-4">
        <div className="rounded-lg border border-[#172334] bg-[#0d1420] px-3.5 py-3">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-medium text-slate-400">
              Investigation Engine
            </p>

            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          </div>

          <p className="mt-1 text-[10px] text-slate-600">
            Operational
          </p>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar