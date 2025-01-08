import { useState, useEffect } from 'react'

export const useTodos = () => {
  const [todos, setTodos] = useState([])

  useEffect(() => {
    const savedTodos = localStorage.getItem('todos')
    console.log('[localStorage.getItem]', {
      key: 'todos',
      rawValue: savedTodos,
      parsedValue: savedTodos ? JSON.parse(savedTodos) : null,
      timestamp: new Date().toISOString()
    })
    if (savedTodos) {
      setTodos(JSON.parse(savedTodos))
    }
  }, [])

  useEffect(() => {
    if (todos.length > 0) {
      console.log('[localStorage.setItem]', {
        key: 'todos',
        value: todos,
        stringifiedValue: JSON.stringify(todos),
        todosCount: todos.length,
        completedCount: todos.filter(t => t.completed).length,
        timestamp: new Date().toISOString()
      })
      localStorage.setItem('todos', JSON.stringify(todos))
    }
  }, [todos])

  const addTodo = (text, dueDate = null) => {
    if (!text.trim()) return
    setTodos([...todos, {
      id: Date.now(),
      text: text.trim(),
      completed: false,
      dueDate
    }])
  }

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  return {
    todos,
    addTodo,
    toggleTodo,
    deleteTodo
  }
}