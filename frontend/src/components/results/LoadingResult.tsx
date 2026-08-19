import type { Task } from '../../types/ui'

interface LoadingResultProps {
  task: Task
}

const labels: Record<Task, string> = {
  sentiment: 'Analyzing sentiment',
  entities: 'Finding named entities',
  classification: 'Classifying text',
}

function LoadingResult({
  task,
}: LoadingResultProps) {
  return (
    <section
      className="result-card loading-result"
      role="status"
      aria-live="polite"
    >
      <div className="loading-spinner" />

      <div>
        <span className="eyebrow">
          Processing
        </span>

        <h2>{labels[task]}</h2>

        <p>
          PolyText is running the request through
          the selected model.
        </p>
      </div>
    </section>
  )
}

export default LoadingResult
