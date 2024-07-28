import ReactDOM from 'react-dom/client'

import './styles/globals.css'

import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { ThemeProvider } from '@/components/theme-provider'

import { Root } from '@/components/root'
import { Home } from '@/pages/home'
import { Game } from '@/pages/game'
import { NotFound } from '@/pages/404'

import { Toaster } from '@/components/ui/toaster'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      {
        element: <Home />,
        index: true
      },
      {
        path: 'games/:gameId',
        element: <Game />
      }
    ]
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  // <React.StrictMode>
  <ThemeProvider defaultTheme="dark" storageKey="bridgebuff-ui-theme">
    <RouterProvider router={router} />
    <Toaster />
  </ThemeProvider>
  // </React.StrictMode>
)
