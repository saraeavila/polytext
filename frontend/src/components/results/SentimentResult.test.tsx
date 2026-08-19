import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import SentimentResult from './SentimentResult'

describe('SentimentResult', () => {
  it('renders the API prediction', () => {
    render(
      <SentimentResult
        latencyMs={243}
        result={{
          language: {
            code: 'es',
            confidence: 0.995,
          },
          sentiment: {
            label: 'positive',
            confidence: 0.976,
          },
        }}
      />,
    )

    expect(
      screen.getByText('Positive', {
        exact: false,
      }),
    ).toBeInTheDocument()

    expect(
      screen.getByText('97.6%'),
    ).toBeInTheDocument()

    expect(
      screen.getByText('Spanish'),
    ).toBeInTheDocument()

    expect(
      screen.getByText('99.5%'),
    ).toBeInTheDocument()

    expect(
      screen.getByText('243 ms'),
    ).toBeInTheDocument()
  })

  it('handles missing language confidence', () => {
    render(
      <SentimentResult
        latencyMs={100}
        result={{
          language: {
            code: 'en',
            confidence: null,
          },
          sentiment: {
            label: 'neutral',
            confidence: 0.72,
          },
        }}
      />,
    )

    expect(
      screen.getByText('English'),
    ).toBeInTheDocument()

    expect(
      screen.getByText('—'),
    ).toBeInTheDocument()
  })
})
