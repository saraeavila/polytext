export type SentimentLabel =
  | 'positive'
  | 'neutral'
  | 'negative'

export interface LanguageInfo {
  code: string
  confidence?: number | null
}

export interface SentimentPrediction {
  label: SentimentLabel
  confidence: number
}

export interface SentimentRequest {
  text: string
  language?: string
}

export interface SentimentResponse {
  language: LanguageInfo
  sentiment: SentimentPrediction
}

export type EntityLabel =
  | 'person'
  | 'organization'
  | 'location'
  | 'miscellaneous'

export interface EntityPrediction {
  text: string
  label: EntityLabel
  start: number
  end: number
  confidence: number
}

export interface NERRequest {
  text: string
  language?: string
}

export interface NERResponse {
  language: LanguageInfo
  entities: EntityPrediction[]
}

export interface ClassificationPrediction {
  label: string
  confidence: number
}

export interface ClassificationRequest {
  text: string
  candidate_labels: string[]
  language?: string
}

export interface ClassificationResponse {
  language: LanguageInfo
  classification: ClassificationPrediction[]
}
