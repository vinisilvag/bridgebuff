import { useState, useEffect } from 'react'

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

import { ContentTable } from '@/components/content-table'

import { type IGame } from '@/interfaces/game'
import { Button } from '@/components/ui/button'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface RankingResponse {
  ranking: string
  limit: number
  start: number
  prev: string | null
  next: string | null
  games: number[]
}

export function Home() {
  const [sort, setSort] = useState('sunk')
  const [fetchUrl, setFetchUrl] = useState(
    `api/rank/${sort}?limit=${10}&start=${1}`
  )
  const [loading, setLoading] = useState(true)
  const [games, setGames] = useState<IGame[]>([])
  const [pagination, setPagination] = useState<{
    ranking: string
    limit: number
    start: number
    prev: string | null
    next: string | null
  } | null>(null)

  const { toast } = useToast()

  async function fetchGames() {
    try {
      setLoading(true)

      const response = await api.get<RankingResponse>(fetchUrl)

      console.log(response.data)

      const gamesIds = response.data.games
      const completeGames: IGame[] = []

      await Promise.all(
        gamesIds.map(async gameId => {
          await api
            .get<{ game_id: number; game_stats: IGame }>(`api/game/${gameId}`)
            .then(gameResponse => {
              completeGames.push(gameResponse.data.game_stats)
            })
        })
      )

      setGames(completeGames)
      setPagination({
        ranking: response.data.ranking,
        limit: response.data.limit,
        start: response.data.start,
        prev: response.data.prev,
        next: response.data.next
      })
    } catch (err) {
      console.log(err)

      toast({
        variant: 'destructive',
        title: 'Falha ao realizar a requisição',
        description: 'Um erro ocorreu enquanto a requisição era feita'
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchGames()
  }, [fetchUrl])

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:gap-0 items-center justify-between">
        <h1 className="text-3xl font-bold">Jogos</h1>

        <Select
          onValueChange={value => {
            setSort(value)
            setFetchUrl(`api/rank/${value}?limit=${10}&start=${1}`)
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
        <ContentTable games={games} loading={loading} />
      </div>

      {pagination && (
        <div className="flex flex-row items-center justify-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            disabled={!pagination.prev}
            onClick={async () => {
              console.log('previous page')
              if (pagination.prev) {
                setFetchUrl(pagination.prev)
              }
            }}
          >
            <ChevronLeft className="h-4 w-4" /> Anterior
          </Button>
          <Button
            size="sm"
            variant="ghost"
            disabled={!pagination.next}
            onClick={async () => {
              console.log('next page')
              if (pagination.next) {
                setFetchUrl(pagination.next)
              }
            }}
          >
            Próximo <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  )
}
