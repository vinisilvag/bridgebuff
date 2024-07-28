export interface IGame {
  id: number
  auth: string
  cannons: number[][]
  escaped_ships: number
  getcannons_received: number
  getturn_received: number
  last_turn: number
  remaining_life_on_escaped_ships: number
  servers_authenticated: number[]
  ship_moves: number
  shot_received: number
  sunk_ships: number
  tstamp_auth_completion: number
  tstamp_auth_start: number
  tstamp_completion: number
  valid_shots: number
}
