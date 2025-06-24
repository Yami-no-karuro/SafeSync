from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_connect
from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_execute

from sqlite3 import Connection

import os
import sys

def print_help():
    print(f"Usage: python3 main.py <command> [<args>]")
    print("Available commands:")
    print("python3 main.py init")
    print("python3 main.py scan <dir>")

def init():
    conn: Connection = sqlite_connect("database/safe-sync-core.db")
    try:
        sqlite_execute(conn, """
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                hash TEXT NOT NULL
            );
        """)

        print("The \"source\" table was successfully created.")
        print("SafeSync is ready.")
    except Exception as e:
        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
    finally:
        conn.close()

def scan_dir(path: str):
    conn: Connection = sqlite_connect("database/safe-sync-core.db")
    try:
        for root, _dirs, files in os.walk(path):
            for file in files:
                filepath: str = os.path.join(root, file)
                filehash: int = fnv1a_file(filepath)

                query: str = "SELECT * FROM sources WHERE source = ?"
                entry: tuple = sqlite_fetchone(conn, query, (filepath,))
                if entry is not None:
                    print(f"File: \"{filepath}\" was already sourced.")
                    print(f"Skipping entry...")
                    continue

                filehash_hex = hex(filehash)[2:]
                query = "INSERT INTO sources (source, hash) VALUES (?, ?);"
                sqlite_execute(conn, query, (filepath, filehash_hex))
    except Exception as e:
        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command: str = sys.argv[1]
    if command == "init":
        init()
    elif command == "scan" and len(sys.argv) == 3:
        path: str = sys.argv[2]
        scan_dir(path)
    else:
        print_help()
        sys.exit(1)
