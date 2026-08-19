import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import TaskTabs from './TaskTabs'

describe('TaskTabs', () => {
  it('shows all supported NLP tasks', () => {
    render(
      <TaskTabs
        activeTask="sentiment"
        onTaskChange={() => undefined}
      />,
    )

    expect(
      screen.getByRole('tab', {
        name: 'Sentiment',
      }),
    ).toBeInTheDocument()

    expect(
      screen.getByRole('tab', {
        name: 'Entities',
      }),
    ).toBeInTheDocument()

    expect(
      screen.getByRole('tab', {
        name: 'Classification',
      }),
    ).toBeInTheDocument()
  })

  it('calls onTaskChange when a task is selected', async () => {
    const user = userEvent.setup()
    const onTaskChange = vi.fn()

    render(
      <TaskTabs
        activeTask="sentiment"
        onTaskChange={onTaskChange}
      />,
    )

    await user.click(
      screen.getByRole('tab', {
        name: 'Entities',
      }),
    )

    expect(onTaskChange).toHaveBeenCalledWith(
      'entities',
    )
  })
})
