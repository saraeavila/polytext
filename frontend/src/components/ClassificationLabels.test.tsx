import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import ClassificationLabels from './ClassificationLabels'

describe('ClassificationLabels', () => {
  it('shows the number of candidate labels', () => {
    render(
      <ClassificationLabels
        value="technology, business, sports"
        onChange={() => undefined}
      />,
    )

    expect(
      screen.getByText('3 / 20'),
    ).toBeInTheDocument()
  })

  it('reports input changes', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()

    render(
      <ClassificationLabels
        value=""
        onChange={onChange}
      />,
    )

    const input = screen.getByRole('textbox', {
      name: 'Candidate labels',
    })

    await user.type(input, 'technology')

    expect(onChange).toHaveBeenCalled()
  })
})
