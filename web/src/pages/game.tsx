import { useParams } from 'react-router-dom'

export function Game() {
  const params = useParams<{ gameId: string }>()

  console.log(params)

  return (
    <div>
      <p>game content</p>
    </div>
  )
}
