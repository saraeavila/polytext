import type { SentimentResponse } from '../../types/api'

interface SentimentResultProps {
  result: SentimentResponse
  latencyMs: number
}

const languageNames: Record<string, string> = {
  en: 'English',
  es: 'Spanish',
}

function SentimentResult({
  result,
  latencyMs,
}: SentimentResultProps) {
  const sentimentConfidence =
    result.sentiment.confidence * 100

  const languageConfidence =
    result.language.confidence == null
      ? null
      : result.language.confidence * 100

  const languageName =
    languageNames[result.language.code] ??
    result.language.code.toUpperCase()

  return (
    <section className="result-card">
      <div className="result-heading">
        <div>
          <span className="eyebrow">Result</span>
          <h2>Sentiment analysis</h2>
        </div>

        <span className="latency">
          {Math.round(latencyMs)} ms
        </span>
      </div>

      <div className="sentiment-summary">
        <span className="sentiment-label">
          {result.sentiment.label}
        </span>

        <strong>
          {sentimentConfidence.toFixed(1)}%
        </strong>

        <span>confidence</span>
      </div>

      <div className="score-track">
        <div
          className="score-fill"
          style={{
            width: `${sentimentConfidence}%`,
          }}
        />
      </div>

      <div className="metadata-grid sentiment-metadata">
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
    </section>
  )
}

export default SentimentResult
