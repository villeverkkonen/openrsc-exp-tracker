require('@testing-library/jest-dom')
require('@testing-library/svelte')
import { render, screen } from '@testing-library/svelte'
import App from './App.svelte'

describe('App', () => {
  it('shows page title', () => {
    render(App)
    const title = screen.getByText('OpenRSC gained overall experience tracker since 8.4.2023')
    expect(title).toBeInTheDocument()
  })
})