import { useState, useEffect } from 'react'
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
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState('')

  useEffect(() => {
    const savedTodos = localStorage.getItem('todos')
    if (savedTodos) {
      setTodos(JSON.parse(savedTodos))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos))
  }, [todos])

  const [dueDate, setDueDate] = useState('')

  const addTodo = (e) => {
    e.preventDefault()
    if (!newTodo.trim()) return

    setTodos([...todos, {
      id: Date.now(),
      text: newTodo.trim(),
      completed: false,
      dueDate: dueDate || null
    }])
    setNewTodo('')
    setDueDate('')
  }

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  return (
    <div className="app">
      <h1>Todo List</h1>
      
      <form onSubmit={addTodo} className="todo-form">
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
