require('@testing-library/jest-dom')
require('@testing-library/svelte')
import { render, screen, waitFor } from '@testing-library/svelte'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import App from './App.svelte'

const mockHiscores = [
  {
    'playerName': 'Lord Jolt',
    'oldExp': 50.0,
    'newExp': 300.0,
    'gainedExp': 250.0
  },
  {
    'playerName': 'Purilainen',
    'oldExp': 100.0,
    'newExp': 200.0,
    'gainedExp': 100.0
  },
  {
    'playerName': 'LeChuck',
    'oldExp': 200.0,
    'newExp': 250.0,
    'gainedExp': 50.0
  }
]

describe('App', () => {
  const server = setupServer(
    rest.get('/api/hiscores', (req, res, ctx) => {
      return res(ctx.status(200), ctx.json(mockHiscores))
    }),
  )

  beforeAll(() => server.listen())
  beforeEach(() => render(App))
  afterEach(() => server.resetHandlers())
  afterAll(() => server.close())

  it('shows page title', () => {
    const title = screen.getByText('OpenRSC gained overall experience tracker since', { exact: false })
    expect(title).toBeInTheDocument()
  })

  it('should show loading text before mounting', () => {
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('shows right amount of cards', async () => {
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).toBeNull()
      expect(screen.getByText('Lord Jolt')).toBeInTheDocument()
      expect(screen.getByText('Purilainen')).toBeInTheDocument()
      expect(screen.getByText('LeChuck')).toBeInTheDocument()
    })
  })
})