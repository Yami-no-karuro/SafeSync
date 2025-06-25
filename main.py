from init import init
from status import status

from sqlite3 import Connection

import sys

def print_help():
    print(f"Usage: python3 main.py <command> [<args>]")
    print("Available commands:")
    print("python3 main.py init <dir>")
    print("python3 main.py status <dir>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command: str = sys.argv[1]
    if command == "init" and len(sys.argv) == 3:
        destination: str = sys.argv[2]
        init(destination)
    elif command == "status" and len(sys.argv) == 3:
        destination: str = sys.argv[2]
        status(destination)
    else:
        print_help()
        sys.exit(1)
