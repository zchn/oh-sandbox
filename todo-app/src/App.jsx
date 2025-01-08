import { useState } from 'react'
import { useTodos } from './hooks/useTodos'
import './App.css'

const formatDate = (dateString) => {
  const options = { weekday: 'short', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const isOverdue = (dateString) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const dueDate = new Date(dateString)
  return dueDate < today
}

function App() {
  const [newTodo, setNewTodo] = useState('')
  const [dueDate, setDueDate] = useState('')
  const { todos, addTodo, toggleTodo, deleteTodo } = useTodos()

  const handleSubmit = (e) => {
    e.preventDefault()
    addTodo(newTodo, dueDate || null)
    setNewTodo('')
    setDueDate('')
  }

  return (
    <div className="app">
      <h1>Todo List</h1>
      
      <form onSubmit={handleSubmit} className="todo-form">
        <div className="input-group">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="What needs to be done?"
            className="todo-input"
          />
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="date-input"
          />
        </div>
        <button type="submit" className="add-button">Add Todo</button>
      </form>

      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className="todo-item">
            <div className="todo-content">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodo(todo.id)}
              />
              <div className="todo-text">
                <span style={{ 
                  textDecoration: todo.completed ? 'line-through' : 'none'
                }}>
                  {todo.text}
                </span>
                {todo.dueDate && (
                  <span className={`due-date ${isOverdue(todo.dueDate) ? 'overdue' : ''}`}>
                    Due: {formatDate(todo.dueDate)}
                  </span>
                )}
              </div>
            </div>
            <button 
              onClick={() => deleteTodo(todo.id)}
              className="delete-button"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
