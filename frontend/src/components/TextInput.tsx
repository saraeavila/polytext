interface TextInputProps {
  value: string
  onChange: (value: string) => void
}

function TextInput({
  value,
  onChange,
}: TextInputProps) {
  return (
    <div className="input-group">
      <div className="input-header">
        <label htmlFor="analysis-text">
          Text
        </label>

        <span>
          {value.length} / 5000
        </span>
      </div>

      <textarea
        id="analysis-text"
        value={value}
        maxLength={5000}
        placeholder="Enter text to analyze..."
        onChange={(event) => onChange(event.target.value)}
      />
    </div>
  )
}

export default TextInput
