interface ClassificationLabelsProps {
  value: string
  onChange: (value: string) => void
}

function ClassificationLabels({
  value,
  onChange,
}: ClassificationLabelsProps) {
  const labels = value
    .split(',')
    .map((label) => label.trim())
    .filter(Boolean)

  return (
    <div className="classification-labels">
      <div className="input-header">
        <label htmlFor="candidate-labels">
          Candidate labels
        </label>

        <span>
          {labels.length} / 20
        </span>
      </div>

      <input
        id="candidate-labels"
        type="text"
        value={value}
        placeholder="technology, business, sports, politics"
        onChange={(event) =>
          onChange(event.target.value)
        }
      />

      <span className="field-help">
        Enter between 2 and 20 labels, separated by commas.
      </span>
    </div>
  )
}

export default ClassificationLabels
