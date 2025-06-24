from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_connect
from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_execute

from src.init import init

from sqlite3 import Connection

import sys

def print_help():
    print(f"Usage: python3 main.py <command> [<args>]")
    print("Available commands:")
    print("python3 main.py init <dir>")
    print("python3 main.py scan <dir>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command: str = sys.argv[1]
    if command == "init" and len(sys.argv) == 3:
        destination: str = sys.argv[2]
        init(destination)
    elif command == "scan" and len(sys.argv) == 3:
        pass
    else:
        print_help()
        sys.exit(1)
