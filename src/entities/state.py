from src.utils.db import fetch_latest_state
from src.utils.db import spawn_state

from sqlite3 import Connection

import sys

def get_latest_state(conn: Connection) -> int:
    state: int | None = fetch_latest_state(conn)
    if state is None:
        print("Unable to fetch the latest state.")
        sys.exit(1)

    return state

def add_state(conn: Connection, lts_state: int, lts_sources: dict) -> int:
    state: int | None = None
    if lts_state == 1 and not lts_sources:
        state = lts_state
    else:
        state = spawn_state(conn)
        if state is None:
            print("Unable to create a new state.")
            sys.exit(1)

    return state
