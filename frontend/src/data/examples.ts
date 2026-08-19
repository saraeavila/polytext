import type { Task } from '../types/ui'

export interface PlaygroundExample {
  label: string
  text: string
  language: string
  candidateLabels?: string
}

export const examples: Record<
  Task,
  PlaygroundExample[]
> = {
  sentiment: [
    {
      label: 'Spanish positive',
      text: 'Me encanta este producto. Es exactamente lo que estaba buscando.',
      language: 'auto',
    },
    {
      label: 'English negative',
      text: 'This is one of the worst products I have ever purchased.',
      language: 'auto',
    },
  ],

  entities: [
    {
      label: 'Spanish entities',
      text: 'Sara trabaja en Microsoft en Madrid.',
      language: 'auto',
    },
    {
      label: 'English entities',
      text: 'Tim Cook visited Apple headquarters in California.',
      language: 'auto',
    },
  ],

  classification: [
    {
      label: 'Technology',
      text: 'Apple announced a new artificial intelligence platform for developers and enterprise customers.',
      language: 'auto',
      candidateLabels:
        'technology, business, sports, politics',
    },
    {
      label: 'Spanish sports',
      text: 'El equipo ganó el campeonato después de una temporada increíble.',
      language: 'auto',
      candidateLabels:
        'sports, politics, technology, finance',
    },
  ],
}
