import { useState } from 'react'

interface ApiKeyInputProps {
  value: string
  onChange: (value: string) => void
}

function ApiKeyInput({
  value,
  onChange,
}: ApiKeyInputProps) {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <div className="api-key-control">
      <div className="input-header">
        <label htmlFor="api-key">
          API key
        </label>

        <span>Session only</span>
      </div>

      <div className="api-key-input-wrapper">
        <input
          id="api-key"
          type={isVisible ? 'text' : 'password'}
          value={value}
          placeholder="poly_sk_..."
          autoComplete="off"
          spellCheck={false}
          onChange={(event) =>
            onChange(event.target.value)
          }
        />

        <button
          type="button"
          className="api-key-toggle"
          aria-label={
            isVisible
              ? 'Hide API key'
              : 'Show API key'
          }
          onClick={() =>
            setIsVisible((current) => !current)
          }
        >
          {isVisible ? 'Hide' : 'Show'}
        </button>
      </div>
    </div>
  )
}

export default ApiKeyInput
