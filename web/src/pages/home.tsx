import { useState, useEffect } from 'react'

import {
  Table,
  TableHead,
  TableHeader,
  TableBody,
  TableRow,
  TableCell
} from '@/components/ui/table'

import {
  Select,
  SelectContent,
  SelectLabel,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'

import { api } from '@/services/api'

import { useToast } from '@/components/ui/use-toast'
import { Link } from 'react-router-dom'

export function Home() {
  const [sort, setSort] = useState('sunk')
  const [games, setGames] = useState<number[]>([])

  const { toast } = useToast()

  useEffect(() => {
    async function fetchGames() {
      try {
        const response = await api.get(`/rank/${sort}?limit=10&start=1`)
        setGames(response.data.games)
      } catch (err) {
        console.log(err)
        toast({
          variant: 'destructive',
          title: 'Falha ao realizar a requisição',
          description: 'Um erro ocorreu enquanto a requisição era feita'
        })
      }
    }

    fetchGames()
  }, [sort])

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:gap-0 items-center justify-between">
        <h1 className="text-3xl font-bold">Jogos</h1>

        <Select
          onValueChange={value => {
            setSort(value)
          }}
          defaultValue={sort}
        >
          <SelectTrigger className="w-full sm:w-[210px]">
            <SelectValue placeholder="Ordenar por" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Ordenar por</SelectLabel>
              <SelectItem value="sunk">Navios afundados</SelectItem>
              <SelectItem value="escaped">Navios que escaparam</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <div className="border rounded-lg">
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
            {games.map(game => (
              <TableRow key={game}>
                <TableCell>
                  <Link className="hover:underline" to={`/games/${game}`}>
                    {game}
                  </Link>
                </TableCell>
                <TableCell>
                  <Link className="hover:underline" to={`/games/${game}`}>
                    ...
                  </Link>
                </TableCell>
                <TableCell>...</TableCell>
                <TableCell>...</TableCell>
                <TableCell>...</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
