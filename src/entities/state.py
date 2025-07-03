from src.utils.db import fetch_states
from src.utils.db import fetch_latest_state
from src.utils.db import fetch_state_by_id 
from src.utils.db import spawn_state

from sqlite3 import Connection

import sys

def get_latest_state(conn: Connection) -> dict:
    state: dict | None = fetch_latest_state(conn)
    if state is None:
        print("Unable to fetch the latest state.")
        sys.exit(1)

    return state
    
def get_states(conn: Connection) -> list:
    return fetch_states(conn)
    
def get_state(conn: Connection, id: int) -> dict | None:
    return fetch_state_by_id(conn, id)

def add_state(conn: Connection, lts_state_id: int, lts_sources: dict) -> dict:
    id: int | None = None
    if lts_state_id == 1 and not lts_sources:
        id = lts_state_id
    else:
        id = spawn_state(conn)
        if id is None:
            print("Unable to create a new state.")
            sys.exit(1)

    state: dict | None = get_state(conn, id)
    if state is None:
        print("Unable to fetch new state data.")
        sys.exit(1)

    return state
