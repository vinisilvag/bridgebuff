import { useState, useEffect } from 'react'

import { useParams } from 'react-router-dom'

import { Scroll } from 'lucide-react'

import { api } from '@/services/api'

import { useToast } from '@/components/ui/use-toast'

import { type IGame } from '@/interfaces/game'
import { Skeleton } from '@/components/ui/skeleton'

interface SectionProps {
  title: string
  children: React.ReactNode
}

interface ItemProps {
  label: string
  content: any
}

function LoadingSkeleton() {
  return (
    <div className="w-full mt-8 flex items-center justify-center">
      <div className="w-full max-w-2xl p-6 border rounded-lg">
        <div className="flex items-center justify-center">
          <Skeleton className="h-5 w-[350px]" />
        </div>

        <div className="flex flex-col gap-6 mt-6">
          {[1, 2, 3].map(index => (
            <div
              key={index}
              className="flex flex-col items-start justify-center"
            >
              <Skeleton className="h-5 w-[170px] mb-2" />

              <div>
                <div className="flex flex-row gap-1">
                  <Skeleton className="h-5 w-[50px]" />
                  <Skeleton className="h-5 w-[180px]" />
                </div>

                <div className="flex flex-row mt-1 gap-1">
                  <Skeleton className="h-5 w-[50px]" />
                  <Skeleton className="h-5 w-[180px]" />
                </div>

                <div className="flex flex-row mt-1 gap-1">
                  <Skeleton className="h-5 w-[50px]" />
                  <Skeleton className="h-5 w-[180px]" />
                </div>

                <div className="flex flex-row mt-1 gap-1">
                  <Skeleton className="h-5 w-[50px]" />
                  <Skeleton className="h-5 w-[180px]" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export function Game() {
  const [game, setGame] = useState<IGame | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const params = useParams<{ gameId: string }>()

  const { toast } = useToast()

  useEffect(() => {
    async function fetchGame() {
      try {
        setLoading(true)
        const response = await api.get<{ game_id: number; game_stats: IGame }>(
          `api/game/${params.gameId}`
        )

        console.log(response.data)

        setGame(response.data.game_stats)
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

    fetchGame()
  }, [])

  function Section({ title, children }: SectionProps) {
    return (
      <div className="flex flex-col items-start justify-center">
        <h2 className="text-xl font-medium mb-2">{title}</h2>
        {children}
      </div>
    )
  }

  function Item({ label, content }: ItemProps) {
    return (
      <div>
        <span className="text-lg text-zinc-400">{label}: </span>
        <span className="text-lg break-all">{content.toString()}</span>
      </div>
    )
  }

  if (loading) {
    return <LoadingSkeleton />
  }

  return (
    <div className="w-full mt-8 flex items-center justify-center">
      <div className="w-full max-w-2xl p-6 border rounded-lg">
        <div className="flex flex-row items-center justify-center gap-4">
          <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center">
            <Scroll className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold">Informações sobre a Partida</span>
        </div>

        {!!game && (
          <div className="flex flex-col gap-6 mt-6">
            <Section title="Geral">
              <Item label="ID" content={game.id} />
              <Item label="GAS" content={game.auth} />
              <Item
                label="Servidores autenticados"
                content={game.servers_authenticated}
              />
              <Item label="Canhões" content={game.cannons} />
              <Item
                label="Chamadas a getcannons"
                content={game.getcannons_received}
              />
              <Item
                label="Chamadas a getturn"
                content={game.getturn_received}
              />
            </Section>

            <Section title="Navios, Tiros e Jogo">
              <Item label="Navios que escaparam" content={game.escaped_ships} />
              <Item
                label="Vida restante nos navios que escaparam"
                content={game.remaining_life_on_escaped_ships}
              />
              <Item label="Movimentos de navios" content={game.ship_moves} />
              <Item label="Navios afundados" content={game.sunk_ships} />
              <Item label="Tiros recebidos" content={game.shot_received} />
              <Item label="Tiros válidos" content={game.valid_shots} />
              <Item label="Último turno" content={game.last_turn} />
            </Section>

            <Section title="Timestamps">
              <Item
                label="Autenticação iniciada"
                content={game.tstamp_auth_start}
              />
              <Item
                label="Autenticação finalizada"
                content={game.tstamp_auth_completion}
              />
              <Item label="Jogo finalizado" content={game.tstamp_completion} />
            </Section>
          </div>
        )}
      </div>
    </div>
  )
}
