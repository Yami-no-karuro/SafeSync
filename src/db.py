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
                state INTEGER NOT NULL,
                obj_path TEXT NOT NULL,
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
        return sqlite_execute(conn, """INSERT INTO sources
            (state, obj_path, path, path_hash, content_hash)
            VALUES (?, ?, ?, ?, ?);
        """, (
            state,
            source["obj_path"],
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
    results: list[tuple] | None = sqlite_fetchall(conn, "SELECT * FROM sources WHERE state = ?;", (state,))
    if results is None:
        return results

    sources: dict = {}
    for source in results:
        sources[source[4]] = {
            "id": source[0],
            "state": source[1],
            "obj_path": source[2],
            "path": source[3],
            "path_hash": source[4],
            "content_hash": source[5]
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
    result: int | None = sqlite_fetchone(conn, "SELECT MAX(id) FROM states;")[0]
    if result is None:
        return sqlite_execute(conn, "INSERT INTO states DEFAULT VALUES;")

    return result
