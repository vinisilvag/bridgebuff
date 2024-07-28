import sys
import csv

from http_requests.http_handler import HttpClientHandler


def GAS_with_best_performance(host, port, output):
    http_handler = HttpClientHandler(host, port)
    first_half = http_handler.make_get_request("/api/rank/sunk?limit=50&start=1")
    second_half = http_handler.make_get_request(first_half["next"])

    games_id = first_half["games"] + second_half["games"]
    immortals = {}

    for game_id in games_id:
        game_data = http_handler.make_get_request(f"/api/game/{game_id}")
        game = game_data["game_stats"]
        if not immortals.get(game["auth"]):
            immortals[game["auth"]] = {"games": 1, "sunk_ships": game["sunk_ships"]}
        else:
            immortals[game["auth"]]["games"] += 1
            immortals[game["auth"]]["sunk_ships"] += game["sunk_ships"]

    for player in immortals:
        immortals[player]["sunk_ships_mean"] = (
            immortals[player]["sunk_ships"] / immortals[player]["games"]
        )

    with open(output, "w") as file:
        writer = csv.writer(file, delimiter=",")
        for player in immortals:
            writer.writerow(
                [
                    player,
                    immortals[player]["games"],
                    immortals[player]["sunk_ships_mean"],
                ]
            )


def best_cannon_placements(host, port):
    http_handler = HttpClientHandler(host, port)

    responce_1 = http_handler.make_get_request("/api/rank/escaped?limit=50&start=1")
    print("\n---------RESPONSE BODY---------\n" + str(responce_1))
    # Transformar o corpo da resposta em um dict e calcular a melhor disposição de canhoes

    pass


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
            best_cannon_placements(ip, port)
        case _:
            print(
                "Invalid analysis command.",
                "\nAvailable commands are: 1 and 2",
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
