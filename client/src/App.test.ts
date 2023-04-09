require('@testing-library/jest-dom')
require('@testing-library/svelte')
import { render, screen, waitFor } from '@testing-library/svelte'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import App from './App.svelte'

const mockHiscores = [
  {
    'playerName': 'Lord Jolt',
    'oldExp': 50,
    'newExp': 300,
    'gainedExp': 250
  },
  {
    'playerName': 'Purilainen',
    'oldExp': 100,
    'newExp': 200,
    'gainedExp': 100
  },
  {
    'playerName': 'LeChuck',
    'oldExp': 200,
    'newExp': 250,
    'gainedExp': 50
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
      expect(screen.getByText('250 exp')).toBeInTheDocument()
      expect(screen.getByText('Purilainen')).toBeInTheDocument()
      expect(screen.getByText('100 exp')).toBeInTheDocument()
      expect(screen.getByText('LeChuck')).toBeInTheDocument()
      expect(screen.getByText('50 exp')).toBeInTheDocument()
    })
  })
})