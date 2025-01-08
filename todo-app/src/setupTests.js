/* eslint-env node */
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  clear: vi.fn()
}

global.localStorage = localStorageMock

// Mock console.log to avoid cluttering test output
global.console.log = vi.fn()