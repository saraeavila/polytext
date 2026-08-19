import {
  useEffect,
  useRef,
  useState,
} from 'react'

import './App.css'

import { ApiError, getHealth } from './api/client'
import { analyzeClassification } from './api/classification'
import { analyzeEntities } from './api/entities'
import { analyzeSentiment } from './api/sentiment'
import ApiKeyInput from './components/ApiKeyInput'
import ClassificationLabels from './components/ClassificationLabels'
import ExamplePrompts from './components/ExamplePrompts'
import Header from './components/Header'
import TaskTabs from './components/TaskTabs'
import TextInput from './components/TextInput'
import ClassificationResult from './components/results/ClassificationResult'
import EntityResult from './components/results/EntityResult'
import LoadingResult from './components/results/LoadingResult'
import SentimentResult from './components/results/SentimentResult'
import { examples } from './data/examples'
import type { ApiStatus, Task } from './types/ui'
import type {
  ClassificationResponse,
  NERResponse,
  SentimentResponse,
} from './types/api'
import type { PlaygroundExample } from './data/examples'

function App() {
  const [activeTask, setActiveTask] =
    useState<Task>('sentiment')

  const [text, setText] = useState(
    'Me encanta este producto. Es exactamente lo que estaba buscando.',
  )

  const [apiStatus, setApiStatus] =
    useState<ApiStatus>('checking')

  const [apiKey, setApiKey] = useState('')

  const [language, setLanguage] = useState('auto')

  const [sentimentResult, setSentimentResult] =
    useState<SentimentResponse | null>(null)

  const [entityResult, setEntityResult] =
    useState<NERResponse | null>(null)

  const [candidateLabels, setCandidateLabels] =
    useState(
      'technology, business, sports, politics',
    )

  const [
    classificationResult,
    setClassificationResult,
  ] = useState<ClassificationResponse | null>(
    null,
  )

  const [isAnalyzing, setIsAnalyzing] =
    useState(false)

  const [analysisError, setAnalysisError] =
    useState<string | null>(null)

  const [latencyMs, setLatencyMs] =
    useState<number | null>(null)

  const parsedCandidateLabels = candidateLabels
    .split(',')
    .map((label) => label.trim())
    .filter(Boolean)

  const abortControllerRef =
    useRef<AbortController | null>(null)

  const requestIdRef = useRef(0)

  useEffect(() => {
    async function checkApi() {
      try {
        await getHealth()
        setApiStatus('ready')
      } catch {
        setApiStatus('offline')
      }
    }

    void checkApi()
  }, [])

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort()
    }
  }, [])

  async function handleAnalyze() {
    if (!text.trim() || !apiKey.trim()) {
      return
    }

    if (
      activeTask === 'classification' &&
      (
        parsedCandidateLabels.length < 2 ||
        parsedCandidateLabels.length > 20
      )
    ) {
      setAnalysisError(
        'Enter between 2 and 20 candidate labels.',
      )
      return
    }

    abortControllerRef.current?.abort()

    const controller = new AbortController()
    abortControllerRef.current = controller

    requestIdRef.current += 1
    const requestId = requestIdRef.current

    setIsAnalyzing(true)
    setAnalysisError(null)

    setSentimentResult(null)
    setEntityResult(null)
    setClassificationResult(null)
    setLatencyMs(null)

    const startedAt = performance.now()

    try {
      const languageRequest =
        language === 'auto'
          ? {}
          : { language }

      if (activeTask === 'sentiment') {
        const result = await analyzeSentiment(
          {
            text: text.trim(),
            ...languageRequest,
          },
          apiKey.trim(),
          controller.signal,
        )

        if (requestId === requestIdRef.current) {
          setSentimentResult(result)
        }
      }

      if (activeTask === 'entities') {
        const result = await analyzeEntities(
          {
            text: text.trim(),
            ...languageRequest,
          },
          apiKey.trim(),
          controller.signal,
        )

        if (requestId === requestIdRef.current) {
          setEntityResult(result)
        }
      }

      if (activeTask === 'classification') {
        const result =
          await analyzeClassification(
            {
              text: text.trim(),
              candidate_labels:
                parsedCandidateLabels,
              ...languageRequest,
            },
            apiKey.trim(),
            controller.signal,
          )

        if (requestId === requestIdRef.current) {
          setClassificationResult(result)
        }
      }

      if (requestId === requestIdRef.current) {
        setLatencyMs(
          performance.now() - startedAt,
        )
      }
    } catch (error) {
      if (
        error instanceof DOMException &&
        error.name === 'AbortError'
      ) {
        return
      }

      if (requestId !== requestIdRef.current) {
        return
      }

      if (error instanceof ApiError) {
        switch (error.status) {
          case 401:
            setAnalysisError(
              'The API key is invalid or inactive.',
            )
            break

          case 403:
            setAnalysisError(
              'This API key is not authorized for the request.',
            )
            break

          case 422:
            setAnalysisError(
              'The request contains invalid input.',
            )
            break

          case 429:
            setAnalysisError(
              'Rate limit exceeded. Try again shortly.',
            )
            break

          case 503:
            setAnalysisError(
              'PolyText is temporarily unavailable.',
            )
            break

          default:
            setAnalysisError(
              `The API returned an error (${error.status}).`,
            )
        }
      } else {
        setAnalysisError(
          'Unable to reach PolyText. Check that the API is running.',
        )
      }
    } finally {
      if (requestId === requestIdRef.current) {
        setIsAnalyzing(false)
        abortControllerRef.current = null
      }
    }
  }

  function handleExampleSelect(
    example: PlaygroundExample,
  ) {
    setText(example.text)
    setLanguage(example.language)

    if (example.candidateLabels) {
      setCandidateLabels(example.candidateLabels)
    }

    setSentimentResult(null)
    setEntityResult(null)
    setClassificationResult(null)
    setAnalysisError(null)
    setLatencyMs(null)
  }

  function handleTaskChange(task: Task) {
    abortControllerRef.current?.abort()
    abortControllerRef.current = null

    requestIdRef.current += 1

    setIsAnalyzing(false)
    setActiveTask(task)

    setSentimentResult(null)
    setEntityResult(null)
    setClassificationResult(null)
    setAnalysisError(null)
    setLatencyMs(null)
  }

  return (
    <div className="app-shell">
      <Header apiStatus={apiStatus} />

      <main className="playground">
        <section className="hero">
          <span className="eyebrow">
            NLP API
          </span>

          <h1>
            Analyze text across languages.
          </h1>

          <p>
            Explore multilingual sentiment,
            named-entity recognition, and
            zero-shot classification through
            PolyText.
          </p>
        </section>

        <div className="workspace">
          <section className="control-card">
            <TaskTabs
              activeTask={activeTask}
              onTaskChange={handleTaskChange}
            />

            <ExamplePrompts
              examples={examples[activeTask]}
              onSelect={handleExampleSelect}
            />

            <TextInput
              value={text}
              onChange={setText}
            />

            {activeTask === 'classification' && (
              <ClassificationLabels
                value={candidateLabels}
                onChange={setCandidateLabels}
              />
            )}

            <ApiKeyInput
              value={apiKey}
              onChange={setApiKey}
            />

            <div className="controls-row">
              <div className="language-control">
                <label htmlFor="language">
                  Language
                </label>

                <select
                  id="language"
                  value={language}
                  onChange={(event) =>
                    setLanguage(event.target.value)
                  }
                >
                  <option value="auto">
                    Auto detect
                  </option>
                  <option value="en">
                    English
                  </option>
                  <option value="es">
                    Spanish
                  </option>
                </select>
              </div>

              <button
                className="analyze-button"
                type="button"
                aria-busy={isAnalyzing}
                disabled={
                  !text.trim() ||
                  !apiKey.trim() ||
                  isAnalyzing ||
                  apiStatus !== 'ready' ||
                  (
                    activeTask === 'classification' &&
                    (
                      parsedCandidateLabels.length < 2 ||
                      parsedCandidateLabels.length > 20
                    )
                  )
                }
                onClick={() => void handleAnalyze()}
              >
                {isAnalyzing ? 'Analyzing…' : 'Analyze'}

                {!isAnalyzing && (
                  <span aria-hidden="true">→</span>
                )}
              </button>
            </div>
          </section>

          {isAnalyzing ? (
            <LoadingResult task={activeTask} />
          ) : activeTask === 'sentiment' ? (
            sentimentResult && latencyMs !== null ? (
              <SentimentResult
                result={sentimentResult}
                latencyMs={latencyMs}
              />
            ) : (
              <section className="result-card empty-result">
                <span className="eyebrow">Result</span>

                <h2>Sentiment analysis</h2>

                {analysisError ? (
                  <p
                    className="error-message"
                    role="alert"
                  >
                    {analysisError}
                  </p>
                ) : (
                  <p>
                    Enter text and analyze it to see
                    the model prediction.
                  </p>
                )}
              </section>
            )
          ) : activeTask === 'entities' ? (
            entityResult && latencyMs !== null ? (
              <EntityResult
                result={entityResult}
                sourceText={text.trim()}
                latencyMs={latencyMs}
              />
            ) : (
              <section className="result-card empty-result">
                <span className="eyebrow">Result</span>

                <h2>Entity recognition</h2>

                {analysisError ? (
                  <p
                    className="error-message"
                    role="alert"
                  >
                    {analysisError}
                  </p>
                ) : (
                  <p>
                    Analyze text to identify people,
                    organizations, locations, and other
                    named entities.
                  </p>
                )}
              </section>
            )
          ) : classificationResult &&
            latencyMs !== null ? (
            <ClassificationResult
              result={classificationResult}
              latencyMs={latencyMs}
            />
          ) : (
            <section className="result-card empty-result">
              <span className="eyebrow">Result</span>

              <h2>Zero-shot classification</h2>

              {analysisError ? (
                <p
                  className="error-message"
                  role="alert"
                >
                  {analysisError}
                </p>
              ) : (
                <p>
                  Provide candidate labels and analyze
                  the text to rank the possible classes.
                </p>
              )}
            </section>
          )}
        </div>
      </main>

      <footer>
        PolyText · Multilingual NLP API
      </footer>
    </div>
  )
}

export default App
