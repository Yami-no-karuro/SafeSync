from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_fetchall
from lib.sqlite import sqlite_execute

from sqlite3 import Connection

import sys

def create_sources_table(conn: Connection):
    try:
        sqlite_execute(conn, """
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state INTEGER,
                path TEXT NOT NULL,
                path_hash TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                FOREIGN KEY (state) REFERENCES states(id) ON DELETE CASCADE
            );
        """)
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)

def add_source(conn: Connection, state: int, source: dict) -> int | None:
    try:
        return sqlite_execute(conn, """INSERT INTO sources (
            state,
            path,
            path_hash,
            content_hash
        ) VALUES (
            ?, ?, ?, ?
        );""", (
            state,
            source["path"],
            source["path_hash"],
            source["content_hash"]
        ))
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
        sys.exit(1)

def get_sources_by_state(conn: Connection, state: int) -> dict | None:
    results: list[tuple] | None = sqlite_fetchall(conn, """
        SELECT * FROM sources
        WHERE state = ?
    """, (state,))

    if results is None:
        return None

    sources: dict = {}
    for source in results:
        sources[source[3]] = {
            "id": source[0],
            "state": source[1],
            "path": source[2],
            "path_hash": source[3],
            "content_hash": source[4]
        }

    return sources

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

def get_latest_state(conn: Connection) -> int | None:
    result: tuple | None = sqlite_fetchone(conn, "SELECT MAX(id) FROM states;")
    if result is None:
        return None

    return result[0]
