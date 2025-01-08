import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useTodos } from './useTodos'

describe('useTodos', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('initializes with empty todos', () => {
    const { result } = renderHook(() => useTodos())
    expect(result.current.todos).toEqual([])
  })

  it('adds a new todo', () => {
    const { result } = renderHook(() => useTodos())
    
    act(() => {
      result.current.addTodo('Test todo')
    })

    expect(result.current.todos).toHaveLength(1)
    expect(result.current.todos[0].text).toBe('Test todo')
    expect(result.current.todos[0].completed).toBe(false)
  })

  it('toggles a todo', () => {
    const { result } = renderHook(() => useTodos())
    
    act(() => {
      result.current.addTodo('Test todo')
    })

    const todoId = result.current.todos[0].id

    act(() => {
      result.current.toggleTodo(todoId)
    })

    expect(result.current.todos[0].completed).toBe(true)
  })

  it('deletes a todo', () => {
    const { result } = renderHook(() => useTodos())
    
    act(() => {
      result.current.addTodo('Test todo')
    })

    const todoId = result.current.todos[0].id

    act(() => {
      result.current.deleteTodo(todoId)
    })

    expect(result.current.todos).toHaveLength(0)
  })

  it('loads todos from localStorage', () => {
    const savedTodos = [
      { id: 1, text: 'Test todo', completed: false }
    ]
    localStorage.getItem.mockReturnValue(JSON.stringify(savedTodos))

    const { result } = renderHook(() => useTodos())
    expect(result.current.todos).toEqual(savedTodos)
  })

  it('saves todos to localStorage when updated', () => {
    const { result } = renderHook(() => useTodos())
    
    act(() => {
      result.current.addTodo('Test todo')
    })

    expect(localStorage.setItem).toHaveBeenCalledWith(
      'todos',
      expect.stringContaining('Test todo')
    )
  })

  it('does not save to localStorage when todos is empty', () => {
    // Mock localStorage.getItem to return null (empty todos)
    localStorage.getItem.mockReturnValue(null)
    
    const { result } = renderHook(() => useTodos())
    
    // Start with empty todos
    expect(result.current.todos).toHaveLength(0)

    // Clear any previous calls to localStorage.setItem
    localStorage.setItem.mockClear()

    // Verify that no localStorage calls are made with empty todos
    act(() => {
      result.current.deleteTodo(123) // Try to delete non-existent todo
    })

    expect(localStorage.setItem).not.toHaveBeenCalled()
  })
})