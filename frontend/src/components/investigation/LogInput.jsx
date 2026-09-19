import { useRef } from 'react'

const MAX_FILE_SIZE = 5 * 1024 * 1024

function LogInput({ value, onChange, disabled, onError }) {
  const fileInputRef = useRef(null)

  async function handleFile(file) {
    if (!file) {
      return
    }

    onError('')

    const extension = file.name.split('.').pop()?.toLowerCase()

    if (!['log', 'txt'].includes(extension)) {
      onError('Please upload a .log or .txt file.')
      return
    }

    if (file.size > MAX_FILE_SIZE) {
      onError('Log files must be smaller than 5 MB.')
      return
    }

    try {
      const text = await file.text()

      if (!text.trim()) {
        onError('The uploaded log file is empty.')
        return
      }

      onChange(text)
    } catch (error) {
      console.error(error)
      onError('Unable to read the uploaded log file.')
    }
  }

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    handleFile(file)

    // Allows selecting the same file again later.
    event.target.value = ''
  }

  function handleDrop(event) {
    event.preventDefault()

    if (disabled) {
      return
    }

    const file = event.dataTransfer.files?.[0]

    handleFile(file)
  }

  function handleDragOver(event) {
    event.preventDefault()
  }

  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <label
          htmlFor="log-input"
          className="text-[13px] font-semibold text-slate-200"
        >
          Security logs
        </label>

        <button
          type="button"
          disabled={disabled}
          onClick={() => fileInputRef.current?.click()}
          className="text-[11px] font-medium text-blue-300 transition hover:text-blue-200 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Upload log file
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".log,.txt,text/plain"
          onChange={handleFileChange}
          disabled={disabled}
          className="hidden"
        />
      </div>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="relative"
      >
        <textarea
          id="log-input"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          disabled={disabled}
          placeholder="Paste security logs here or drop a .log / .txt file..."
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
      </div>

      <div className="mt-3 flex items-center justify-between">
        <p className="text-[11px] text-slate-600">
          Supports .log and .txt files up to 5 MB
        </p>

        <p className="font-mono text-[11px] text-slate-600">
          {value.length.toLocaleString()} characters
        </p>
      </div>
    </div>
  )
}

export default LogInput