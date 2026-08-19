import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import LoadingResult from './LoadingResult'

describe('LoadingResult', () => {
  it('shows the active task', () => {
    render(
      <LoadingResult task="classification" />,
    )

    expect(
      screen.getByRole('status'),
    ).toBeInTheDocument()

    expect(
      screen.getByText('Classifying text'),
    ).toBeInTheDocument()
  })
})
