import sys
import csv
from collections import defaultdict
from http_requests.http_handler import HttpClientHandler
from helpers.cannon_placement import normalize_cannon_placements

def GAS_with_best_performance(host, port, output):
    http_handler = HttpClientHandler(host, port)
    url = "/api/rank/sunk?limit=50&start=1"
    top = 100

    games_id = []

    while len(games_id) < top:
        response = http_handler.make_get_request(url)
        games_id += response["games"]
        url = response["next"]

    games_id = games_id[0:top]
    immortals = {}

    for game_id in games_id:
        game_data = http_handler.make_get_request(f"/api/game/{game_id}")
        game = game_data["game_stats"]
        if game["auth"] not in immortals:
            immortals[game["auth"]] = {"games": 1, "sunk_ships": game["sunk_ships"]}
        else:
            immortals[game["auth"]]["games"] += 1
            immortals[game["auth"]]["sunk_ships"] += game["sunk_ships"]

    for player in immortals:
        immortals[player]["sunk_ships_average"] = (
            immortals[player]["sunk_ships"] / immortals[player]["games"]
        )

    # properly sort this

    with open(output, "w") as file:
        writer = csv.writer(file, delimiter=",")
        for player in immortals:
            writer.writerow(
                [
                    player,
                    immortals[player]["games"],
                    immortals[player]["sunk_ships_average"],
                ]
            )


def best_cannon_placements(host, port, output):
    http_handler = HttpClientHandler(host, port)

    # Obtem os top100 com melhor desempenho (menos navios escapados)
    responce_1 = http_handler.make_get_request("/api/rank/escaped?limit=50&start=1")
    responce_2 = http_handler.make_get_request("/api/rank/escaped?limit=50&start=1")
    all_games = responce_1['games'] + responce_2['games']

    normalised_canonons = []
    for game in all_games:
        
        # Obtém as estatisticas de um jogo especifico dentre os top100
        game_body = http_handler.make_get_request(f"/api/game/{game}")
        
        # Obtem a possicao normalizada dos canhoes
        cannons = game_body.get('game_stats').get('cannons')
        normalized_cannon_placement = normalize_cannon_placements(cannons)
        
        # Obtem o numero de navios escapados
        num_escaped_ships = game_body.get('game_stats').get('escaped_ships')

        # Armazena os canhoes normalizados e o numero de navios escapados
        normalised_canonons.append((normalized_cannon_placement, num_escaped_ships))
        
    # Dicionários para armazenar a soma dos navios que escaparam e o número de ocorrências por posição de canhões
    soma_navios_por_posicao = defaultdict(int)
    contagem_por_posicao = defaultdict(int)

    # Agrupar e somar os navios que escaparam por posição, contando o número de ocorrências
    for posicao, navios in normalised_canonons:
        soma_navios_por_posicao[posicao] += navios
        contagem_por_posicao[posicao] += 1

    # Calcular a média de navios que escaparam por posição
    media_navios_por_posicao = {posicao: soma_navios_por_posicao[posicao] / contagem_por_posicao[posicao]
                                for posicao in soma_navios_por_posicao}
    
    # Ordenar os resultados pela média de navios escapados
    media_navios_ordenada = sorted(media_navios_por_posicao.items(), key=lambda x: x[1])

    #print(media_navios_ordenada)

    # Salvar o resultado em um arquivo CSV
    with open(output, mode='w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)

        for posicao, media in media_navios_ordenada:
            escritor_csv.writerow([posicao, media])


def main() -> None:
    if len(sys.argv) - 1 != 4:
        print(
            "Invalid arguments.",
            "\nCorrect usage is: python3 client.py <IP> <PORT> <ANALYSIS> <OUTPUT>",
        )
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    analysis = int(sys.argv[3])
    output = sys.argv[4]

    # print(ip, port, analysis, output)

    match analysis:
        case 1:
            GAS_with_best_performance(ip, port, output)
        case 2:
            best_cannon_placements(ip, port, output)
        case _:
            print(
                "Invalid analysis command.",
                "\nAvailable commands are: 1 and 2",
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
