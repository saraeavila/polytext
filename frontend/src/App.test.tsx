import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest'

import App from './App'

function jsonResponse(
  body: unknown,
  status = 200,
): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

const fetchMock = vi.fn()

beforeEach(() => {
  fetchMock.mockReset()
  vi.stubGlobal('fetch', fetchMock)
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('App', () => {
  it('shows API ready once the health check succeeds', async () => {
    fetchMock.mockImplementation(async (input) => {
      const url = String(input)

      if (url.endsWith('/health')) {
        return jsonResponse({ status: 'healthy' })
      }

      return jsonResponse({}, 404)
    })

    render(<App />)

    expect(
      screen.getByText('Checking API'),
    ).toBeInTheDocument()

    await screen.findByText('API ready')
  })

  it('shows API offline when the health check fails', async () => {
    fetchMock.mockImplementation(async (input) => {
      const url = String(input)

      if (url.endsWith('/health')) {
        return jsonResponse({}, 503)
      }

      return jsonResponse({}, 404)
    })

    render(<App />)

    await screen.findByText('API offline')
  })

  it('runs a sentiment analysis and renders the prediction', async () => {
    const user = userEvent.setup()

    fetchMock.mockImplementation(async (input) => {
      const url = String(input)

      if (url.endsWith('/health')) {
        return jsonResponse({ status: 'healthy' })
      }

      if (url.endsWith('/v1/sentiment')) {
        return jsonResponse({
          language: { code: 'es', confidence: 0.99 },
          sentiment: {
            label: 'positive',
            confidence: 0.976,
          },
        })
      }

      return jsonResponse({}, 404)
    })

    render(<App />)

    await screen.findByText('API ready')

    await user.type(
      screen.getByLabelText('API key'),
      'poly_sk_test',
    )

    await user.click(
      screen.getByRole('button', {
        name: /analyze/i,
      }),
    )

    await screen.findByText('97.6%')

    expect(
      screen.getByText('Spanish', {
        selector: 'strong',
      }),
    ).toBeInTheDocument()
  })

  it('sends the parsed candidate labels for classification', async () => {
    const user = userEvent.setup()

    fetchMock.mockImplementation(async (input) => {
      const url = String(input)

      if (url.endsWith('/health')) {
        return jsonResponse({ status: 'healthy' })
      }

      if (url.endsWith('/v1/classify')) {
        return jsonResponse({
          language: { code: 'en', confidence: 0.98 },
          classification: [
            { label: 'technology', confidence: 0.9 },
          ],
        })
      }

      return jsonResponse({}, 404)
    })

    render(<App />)

    await screen.findByText('API ready')

    await user.click(
      screen.getByRole('tab', {
        name: 'Classification',
      }),
    )

    await user.type(
      screen.getByLabelText('API key'),
      'poly_sk_test',
    )

    await user.click(
      screen.getByRole('button', {
        name: /analyze/i,
      }),
    )

    await screen.findByText('90.0%')

    const classificationCall = fetchMock.mock.calls.find(
      (call) =>
        String(call[0]).endsWith('/v1/classify'),
    )

    expect(
      classificationCall,
    ).toBeDefined()

    const [, options] =
      classificationCall!

    const requestBody = JSON.parse(
      options?.body as string,
    )

    expect(
      requestBody.candidate_labels,
    ).toEqual([
      'technology',
      'business',
      'sports',
      'politics',
    ])
  })

  it('shows a useful error for an invalid API key', async () => {
    const user = userEvent.setup()

    fetchMock.mockImplementation(
      async (input) => {
        const url = String(input)

        if (url.endsWith('/health')) {
          return jsonResponse({
            status: 'healthy',
          })
        }

        if (url.endsWith('/v1/sentiment')) {
          return jsonResponse(
            {
              detail:
                'Invalid API key',
            },
            401,
          )
        }

        return jsonResponse(
          {},
          404,
        )
      },
    )

    render(<App />)

    await screen.findByText('API ready')

    await user.type(
      screen.getByLabelText('API key'),
      'poly_sk_invalid',
    )

    await user.click(
      screen.getByRole('button', {
        name: /analyze/i,
      }),
    )

    const error =
      await screen.findByRole('alert')

    expect(error).toHaveTextContent(
      'The API key is invalid or inactive.',
    )
  })
})
