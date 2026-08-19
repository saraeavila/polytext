import { apiRequest } from './client'
import type {
  ClassificationRequest,
  ClassificationResponse,
} from '../types/api'

export async function analyzeClassification(
  request: ClassificationRequest,
  apiKey: string,
  signal?: AbortSignal,
): Promise<ClassificationResponse> {
  return apiRequest<ClassificationResponse>(
    '/v1/classify',
    {
      method: 'POST',
      body: JSON.stringify(request),
      signal,
    },
    apiKey,
  )
}
