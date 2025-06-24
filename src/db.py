from lib.sqlite import sqlite_connect
from lib.sqlite import sqlite_execute
from lib.sqlite import sqlite_fetchone

from sqlite3 import Connection

import sys

def create_sources_table(conn: Connection):
    try:
        sqlite_execute(conn, """
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state INTEGER,
                path TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (state) REFERENCES states(id) ON DELETE CASCADE
            );
        """)
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)

def add_source(conn: Connection, state: int, path: str, content: str) -> int | None:
    try:
        return sqlite_execute(conn, """
            INSERT INTO sources (
                state,
                path,
                content
            ) VALUES (
                ?,
                ?,
                ?
            );
        """, (state, path, content))
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)

def create_states_table(conn: Connection):
    try:
        sqlite_execute(conn, """
            CREATE TABLE IF NOT EXISTS states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)

def add_state(conn: Connection) -> int | None:
    try:
        return sqlite_execute(conn, "INSERT INTO states DEFAULT VALUES;")
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)
