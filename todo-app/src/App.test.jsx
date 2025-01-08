import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

describe('App', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders the todo form', () => {
    render(<App />)
    expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /add todo/i })).toBeInTheDocument()
  })

  it('adds a new todo when form is submitted', () => {
    render(<App />)
    const input = screen.getByPlaceholderText('What needs to be done?')
    const button = screen.getByRole('button', { name: /add todo/i })

    fireEvent.change(input, { target: { value: 'Test todo' } })
    fireEvent.click(button)

    expect(screen.getByText('Test todo')).toBeInTheDocument()
  })

  it('marks a todo as completed when checkbox is clicked', () => {
    render(<App />)
    const input = screen.getByPlaceholderText('What needs to be done?')
    const button = screen.getByRole('button', { name: /add todo/i })

    fireEvent.change(input, { target: { value: 'Test todo' } })
    fireEvent.click(button)

    const checkbox = screen.getByRole('checkbox')
    fireEvent.click(checkbox)

    expect(checkbox).toBeChecked()
  })

  it('deletes a todo when delete button is clicked', () => {
    render(<App />)
    const input = screen.getByPlaceholderText('What needs to be done?')
    const button = screen.getByRole('button', { name: /add todo/i })

    fireEvent.change(input, { target: { value: 'Test todo' } })
    fireEvent.click(button)

    const deleteButton = screen.getByRole('button', { name: /delete/i })
    fireEvent.click(deleteButton)

    expect(screen.queryByText('Test todo')).not.toBeInTheDocument()
  })
})