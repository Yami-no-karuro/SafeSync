from src.db import fetch_sources_by_state
from src.db import spawn_source

from sqlite3 import Connection

import sys

def get_latest_sources(conn: Connection, state: int) -> dict:
    sources: dict | None = fetch_sources_by_state(conn, state)
    if sources is None:
        sources = {}

    return sources

def add_source(conn: Connection, state: int, source: dict) -> dict:
    id: int | None = spawn_source(conn, state, {
        "obj_path": source["obj_path"],
        "path": source["file_path"],
        "path_hash": source["file_path_hash"],
        "content_hash": source["content_hash"]
    })

    if id is None:
        print("Unable to create a new source in the current state.")
        print("Exiting...")
        sys.exit(1)
        
    source["id"] = id
    return source
