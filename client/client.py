import sys
from http_requests.http_handler import HttpClientHandler

def GAS_with_best_performance(host, port):
    pass
    

def best_cannon_placements(host, port):
    http_handler = HttpClientHandler(host, port)

    response = http_handler.make_get_request("/api/rank/sunk?limit=10&start=1")
    print("HTTP Response:")
    print(response)



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

    #print(ip, port, analysis, output)

    match analysis:
        case 1:
            GAS_with_best_performance(ip, port)
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
