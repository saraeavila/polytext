import type { PlaygroundExample } from '../data/examples'

interface ExamplePromptsProps {
  examples: PlaygroundExample[]
  onSelect: (example: PlaygroundExample) => void
}

function ExamplePrompts({
  examples,
  onSelect,
}: ExamplePromptsProps) {
  return (
    <div className="example-prompts">
      <span className="example-label">
        Try an example
      </span>

      <div className="example-buttons">
        {examples.map((example) => (
          <button
            key={example.label}
            type="button"
            className="example-button"
            onClick={() => onSelect(example)}
          >
            {example.label}
          </button>
        ))}
      </div>
    </div>
  )
}

export default ExamplePrompts
