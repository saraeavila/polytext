import { apiRequest } from './client'
import type {
  NERRequest,
  NERResponse,
} from '../types/api'

export async function analyzeEntities(
  request: NERRequest,
  apiKey: string,
  signal?: AbortSignal,
): Promise<NERResponse> {
  return apiRequest<NERResponse>(
    '/v1/entities',
    {
      method: 'POST',
      body: JSON.stringify(request),
      signal,
    },
    apiKey,
  )
}
