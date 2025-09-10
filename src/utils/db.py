import sys
from sqlite3 import Connection

from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_fetchall
from lib.sqlite import sqlite_execute

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
                update_type INTEGER NOT NULL,
                FOREIGN KEY (state) REFERENCES states(id) ON DELETE CASCADE
            );
        """)
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)

def spawn_source(conn: Connection, state: int, source: dict) -> int | None:
    try:
        return sqlite_execute(conn, """INSERT INTO sources
            (state, obj_path, path, path_hash, content_hash, update_type)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (
            state,
            source["obj_path"],
            source["path"],
            source["path_hash"],
            source["content_hash"],
            source["update_type"]
        ))
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)

def fetch_sources_by_state(conn: Connection, state: int) -> dict | None:
    try:
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
                "content_hash": source[5],
                "update_type": source[6]
            }
    
        return sources
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
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

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)

def spawn_state(conn: Connection) -> int | None:
    try:
        return sqlite_execute(conn, "INSERT INTO states DEFAULT VALUES;")
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)
        
def fetch_state_by_id(conn: Connection, id: int) -> dict | None:
    try:
        result: tuple | None = sqlite_fetchone(conn, "SELECT * FROM states WHERE id = ?;", (id,))
        if result is None:
            return result
            
        return {"id": result[0], "time": result[1]}
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)
        
def fetch_states(conn: Connection) -> list:
    try:
        results: list[tuple] | None = sqlite_fetchall(conn, "SELECT * FROM states;")
        if results is None:
            return []
           
        states: list = []
        for result in results:
            states.append({
                "id": result[0],
                "time": result[1]
            })
    
        return states
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)

def fetch_latest_state(conn: Connection) -> dict | None:
    try:
        result: tuple | None = sqlite_fetchone(conn, """
            SELECT * FROM states
            WHERE id = (
                SELECT MAX(id) FROM states
            );
        """)
        
        if result is None:
            return result
            
        return {"id": result[0], "time": result[1]}
    except Exception as e:
        conn.close()

        print(f"An unexpected error occurred: \"{e}\".")
        sys.exit(1)
