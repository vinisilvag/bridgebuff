import {
  Table,
  TableHead,
  TableHeader,
  TableBody,
  TableRow,
  TableCell
} from '@/components/ui/table'

import { Skeleton } from '@/components/ui/skeleton'

import { Link } from 'react-router-dom'

import { type IGame } from '@/interfaces/game'

interface ContentTableProps {
  games: IGame[]
  loading: boolean
}

export function ContentTable({ games, loading }: ContentTableProps) {
  function clamp(str: string, length: number): string {
    return str.length > length ? str.substring(0, length) + '...' : str
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>GAS</TableHead>
          <TableHead>Navios afundados</TableHead>
          <TableHead>Navios que escaparam</TableHead>
          <TableHead>Vida restante</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        {loading
          ? [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(index => (
              <TableRow key={index}>
                <TableCell>
                  <Skeleton className="h-4 w-[50px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[240px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[50px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[50px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[50px]" />
                </TableCell>
              </TableRow>
            ))
          : games.map(game => (
              <TableRow key={game.id}>
                <TableCell>
                  <Link
                    className="hover:underline line-clamp-2"
                    to={`/games/${game.id}`}
                  >
                    {game.id}
                  </Link>
                </TableCell>
                <TableCell>
                  <Link className="hover:underline" to={`/games/${game.id}`}>
                    {clamp(game.auth, 40)}
                  </Link>
                </TableCell>
                <TableCell>{game.sunk_ships}</TableCell>
                <TableCell>{game.escaped_ships}</TableCell>
                <TableCell>{game.remaining_life_on_escaped_ships}</TableCell>
              </TableRow>
            ))}
      </TableBody>
    </Table>
  )
}
