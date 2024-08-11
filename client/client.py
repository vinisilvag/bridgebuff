import csv
import sys

from helpers.cannon_placement import normalize_cannon_placements
from http_requests.http_handler import HttpClientHandler


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

    # sorted in decreasing order of number of games
    immortals_sorted = sorted(
        immortals.items(), key=lambda item: item[1]["games"], reverse=True
    )

    with open(output, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        for player, stats in immortals_sorted:
            writer.writerow(
                [
                    player,
                    stats["games"],
                    stats["sunk_ships_average"],
                ]
            )


def best_cannon_placements(host, port, output):
    http_handler = HttpClientHandler(host, port)
    url = "/api/rank/escaped?limit=50&start=1"
    top = 100

    games_id = []

    while len(games_id) < top:
        response = http_handler.make_get_request(url)
        games_id += response["games"]
        url = response["next"]

    games_id = games_id[0:top]
    top_meta = {}

    for game_id in games_id:
        game_data = http_handler.make_get_request(f"/api/game/{game_id}")
        game = game_data["game_stats"]

        normalized_cannon_placement = normalize_cannon_placements(game["cannons"])

        if normalized_cannon_placement not in top_meta:
            top_meta[normalized_cannon_placement] = {
                "games": 1,
                "escaped_ships": game["escaped_ships"],
            }
        else:
            top_meta[normalized_cannon_placement]["games"] += 1
            top_meta[normalized_cannon_placement]["escaped_ships"] += game[
                "escaped_ships"
            ]

    for placement in top_meta:
        top_meta[placement]["escaped_ships_average"] = (
            top_meta[placement]["escaped_ships"] / top_meta[placement]["games"]
        )

    # sorted in decreasing order of number of games
    top_meta_sorted = sorted(
        top_meta.items(), key=lambda item: item[1]["escaped_ships"]
    )

    with open(output, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        for placement, stats in top_meta_sorted:
            writer.writerow(
                [
                    placement,
                    stats["escaped_ships_average"],
                ]
            )


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
