from init import init
from snap import snap
from status import status

import sys

def print_help():
    print(f"Usage: safesync <command> [<args>]")
    print("Available commands:")
    print("safesync init <dir>")
    print("safesync status <dir>")
    print("safesync snap <dir>")

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
    elif command == "snap" and len(sys.argv) == 3:
        destination: str = sys.argv[2]
        snap(destination)
    else:
        print_help()
        sys.exit(1)
