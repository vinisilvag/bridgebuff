import socket
import struct
import sys


def GAS_with_best_performance():
    # build and send the request and listen to the server response
    pass


def best_cannon_placements():
    # build and send the request and listen to the server response
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

    print(ip, port, analysis, output)

    match analysis:
        case 1:
            GAS_with_best_performance()
        case 2:
            best_cannon_placements()
        case _:
            print(
                "Invalid analysis command.",
                "\nAvailable commands are: 1 and 2",
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
