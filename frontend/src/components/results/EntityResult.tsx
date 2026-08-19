import type { ReactNode } from 'react'

import type {
  EntityPrediction,
  NERResponse,
} from '../../types/api'

interface EntityResultProps {
  result: NERResponse
  sourceText: string
  latencyMs: number
}

function buildHighlightedText(
  text: string,
  entities: EntityPrediction[],
): ReactNode[] {
  const sortedEntities = [...entities].sort(
    (a, b) => a.start - b.start,
  )

  const nodes: ReactNode[] = []
  let cursor = 0

  sortedEntities.forEach((entity, index) => {
    if (entity.start < cursor) {
      return
    }

    if (entity.start > cursor) {
      nodes.push(
        text.slice(cursor, entity.start),
      )
    }

    nodes.push(
      <span
        className={`entity-highlight entity-${entity.label}`}
        key={`${entity.start}-${entity.end}-${index}`}
      >
        {text.slice(entity.start, entity.end)}
      </span>,
    )

    cursor = entity.end
  })

  if (cursor < text.length) {
    nodes.push(text.slice(cursor))
  }

  return nodes
}

function EntityResult({
  result,
  sourceText,
  latencyMs,
}: EntityResultProps) {
  return (
    <section className="result-card">
      <div className="result-heading">
        <div>
          <span className="eyebrow">Result</span>
          <h2>Entity recognition</h2>
        </div>

        <span className="latency">
          {Math.round(latencyMs)} ms
        </span>
      </div>

      <div className="entity-text-container">
        <span className="metadata-label">
          Annotated text
        </span>

        <p className="entity-text">
          {result.entities.length > 0
            ? buildHighlightedText(
                sourceText,
                result.entities,
              )
            : sourceText}
        </p>
      </div>

      {result.entities.length > 0 ? (
        <div className="entity-list">
          {result.entities.map((entity, index) => (
            <div
              className="entity-row"
              key={`${entity.start}-${entity.end}-${index}`}
            >
              <div className="entity-row-main">
                <span
                  className={`entity-badge entity-${entity.label}`}
                >
                  {entity.label}
                </span>

                <strong>{entity.text}</strong>
              </div>

              <div className="entity-details">
                <span>
                  {(entity.confidence * 100).toFixed(1)}%
                </span>

                <span>
                  {entity.start}:{entity.end}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="no-entities">
          No named entities were detected.
        </p>
      )}
    </section>
  )
}

export default EntityResult
