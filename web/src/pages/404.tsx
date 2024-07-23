import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <div className="w-full h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-xl font-bold">404 - Página não encontrada :(</h1>
      <p className="text-lg">
        Voltar para o{' '}
        <Link to="/" className="text-red-600 hover:underline">
          início
        </Link>
        .
      </p>
    </div>
  )
}
