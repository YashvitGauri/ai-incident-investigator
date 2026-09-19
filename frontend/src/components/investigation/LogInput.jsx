function LogInput({ value, onChange, disabled }) {
  return (
    <div>
      <textarea
        id="log-input"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        placeholder="Paste security logs here..."
        spellCheck="false"
        className="
          h-64
          w-full
          resize-none
          rounded-lg
          border
          border-[#243246]
          bg-[#080d15]
          px-4
          py-4
          font-mono
          text-[13px]
          leading-6
          text-slate-300
          outline-none
          transition
          placeholder:text-slate-700
          focus:border-[#45678f]
          focus:ring-1
          focus:ring-[#45678f]/30
          disabled:cursor-not-allowed
          disabled:opacity-60
        "
      />

      <div className="mt-3 flex items-center justify-between">
        <p className="text-[11px] text-slate-600">
          Supported input: raw security log text
        </p>

        <p className="font-mono text-[11px] text-slate-600">
          {value.length.toLocaleString()} characters
        </p>
      </div>
    </div>
  )
}

export default LogInput