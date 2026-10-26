import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import App from './App'

vi.stubGlobal(
  'fetch',
  vi.fn(() => Promise.reject(new Error('API server is not running during the unit test'))),
)

describe('App', () => {
  it('redirects an unauthenticated visitor to login', async () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>,
    )

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '로그인' })).toBeInTheDocument()
    })
  })
})

