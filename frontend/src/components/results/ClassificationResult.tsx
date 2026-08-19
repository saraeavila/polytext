import type { ClassificationResponse } from '../../types/api'

interface ClassificationResultProps {
  result: ClassificationResponse
  latencyMs: number
}

const languageNames: Record<string, string> = {
  en: 'English',
  es: 'Spanish',
}

function ClassificationResult({
  result,
  latencyMs,
}: ClassificationResultProps) {
  const languageName =
    languageNames[result.language.code] ??
    result.language.code.toUpperCase()

  const languageConfidence =
    result.language.confidence == null
      ? null
      : result.language.confidence * 100

  const sortedPredictions = [
    ...result.classification,
  ].sort(
    (a, b) => b.confidence - a.confidence,
  )

  return (
    <section className="result-card">
      <div className="result-heading">
        <div>
          <span className="eyebrow">Result</span>
          <h2>Zero-shot classification</h2>
        </div>

        <span className="latency">
          {Math.round(latencyMs)} ms
        </span>
      </div>

      <div className="metadata-grid">
        <div>
          <span className="metadata-label">
            Language
          </span>
          <strong>{languageName}</strong>
        </div>

        <div>
          <span className="metadata-label">
            Language code
          </span>
          <strong>{result.language.code}</strong>
        </div>

        <div>
          <span className="metadata-label">
            Detection confidence
          </span>
          <strong>
            {languageConfidence == null
              ? '—'
              : `${languageConfidence.toFixed(1)}%`}
          </strong>
        </div>
      </div>

      <div className="classification-list">
        {sortedPredictions.map(
          (prediction, index) => {
            const confidence =
              prediction.confidence * 100

            return (
              <div
                className="classification-row"
                key={`${prediction.label}-${index}`}
              >
                <div className="classification-label-row">
                  <span>{prediction.label}</span>

                  <strong>
                    {confidence.toFixed(1)}%
                  </strong>
                </div>

                <div className="score-track">
                  <div
                    className="score-fill"
                    style={{
                      width: `${confidence}%`,
                    }}
                  />
                </div>
              </div>
            )
          },
        )}
      </div>
    </section>
  )
}

export default ClassificationResult
