# Todo App

A simple, modern todo list application built with React and Vite. This app allows you to manage your tasks with a clean and intuitive interface.

## Features

- Add new todos with optional due dates
- Mark todos as complete/incomplete
- Delete todos
- Due date tracking with overdue status
- Persistent storage using localStorage (your todos remain saved even after closing the browser)
- Clean, modern UI with proper styling
- Responsive design
- Accessibility features (focus states, semantic HTML)

## Getting Started

### Prerequisites

Make sure you have [Node.js](https://nodejs.org/) installed on your system.

### Installation

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd todo-app
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

### Running the App

To start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or another port if 5173 is already in use).

### Running Tests

The app includes a comprehensive test suite using Vitest and React Testing Library. To run the tests:

```bash
# Run tests in watch mode (development)
npm test

# Run tests with coverage report
npm test:coverage
```

The test suite includes:
- Component tests for the main App
- Custom hook tests for useTodos
- Integration tests for localStorage functionality

## Built With

- [React](https://react.dev/) - The web framework used
- [Vite](https://vitejs.dev/) - Build tool and development server
- localStorage - For data persistence
- [Vitest](https://vitest.dev/) - Testing framework
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) - React component testing
- [Jest DOM](https://github.com/testing-library/jest-dom) - DOM testing utilities
