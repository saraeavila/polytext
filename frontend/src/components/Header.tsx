import type { ApiStatus } from '../types/ui'

interface HeaderProps {
  apiStatus: ApiStatus
}

const statusLabels: Record<ApiStatus, string> = {
  checking: 'Checking API',
  ready: 'API ready',
  offline: 'API offline',
}

function Header({ apiStatus }: HeaderProps) {
  return (
    <header className="app-header">
      <div>
        <div className="brand-row">
          <span className="brand-mark">P</span>
          <span className="brand-name">PolyText</span>
        </div>

        <p className="brand-description">
          Multilingual NLP Playground
        </p>
      </div>

      <div className={`api-status api-status-${apiStatus}`}>
        <span className="status-dot" />
        {statusLabels[apiStatus]}
      </div>
    </header>
  )
}

export default Header
