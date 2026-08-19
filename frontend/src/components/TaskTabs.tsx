import type { Task } from '../types/ui'

interface TaskTabsProps {
  activeTask: Task
  onTaskChange: (task: Task) => void
}

const tasks: { id: Task; label: string }[] = [
  { id: 'sentiment', label: 'Sentiment' },
  { id: 'entities', label: 'Entities' },
  { id: 'classification', label: 'Classification' },
]

function TaskTabs({
  activeTask,
  onTaskChange,
}: TaskTabsProps) {
  return (
    <div
      className="task-tabs"
      role="tablist"
      aria-label="NLP task"
    >
      {tasks.map((task) => (
        <button
          key={task.id}
          type="button"
          role="tab"
          aria-selected={activeTask === task.id}
          className={
            activeTask === task.id
              ? 'task-tab task-tab-active'
              : 'task-tab'
          }
          onClick={() => onTaskChange(task.id)}
        >
          {task.label}
        </button>
      ))}
    </div>
  )
}

export default TaskTabs
