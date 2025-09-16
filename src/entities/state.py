import sys
from sqlite3 import Connection

from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_fetchall
from lib.sqlite import sqlite_execute

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

def add_state(conn: Connection, lts_state_id: int, lts_sources: dict) -> dict:
    id: int | None = None
    if lts_state_id == 1 and not lts_sources:
        id = lts_state_id
    else:
        id = spawn_state(conn)
        if id is None:
            print("Unable to create a new state.")
            sys.exit(1)
            
    state: dict | None = fetch_state_by_id(conn, id)
    if state is None:
        print("Unable to fetch new state data.")
        sys.exit(1)
        
    return state
