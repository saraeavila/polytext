import { apiRequest } from './client'
import type {
  SentimentRequest,
  SentimentResponse,
} from '../types/api'

export async function analyzeSentiment(
  request: SentimentRequest,
  apiKey: string,
  signal?: AbortSignal,
): Promise<SentimentResponse> {
  return apiRequest<SentimentResponse>(
    '/v1/sentiment',
    {
      method: 'POST',
      body: JSON.stringify(request),
      signal,
    },
    apiKey,
  )
}
