import sys
from sqlite3 import Connection

from src.utils.db import fetch_sources_by_state
from src.utils.db import spawn_source

def get_sources(conn: Connection, state_id: int) -> dict:
    sources: dict | None = fetch_sources_by_state(conn, state_id)
    if sources is None:
        sources = {}

    return sources

def add_source(conn: Connection, state_id: int, source: dict) -> dict:
    id: int | None = spawn_source(conn, state_id, {
        "obj_path": source.get("obj_path"),
        "path": source["path"],
        "path_hash": source["path_hash"],
        "content_hash": source.get("content_hash"),
        "update_type": source["update_type"]
    })

    if id is None:
        print("Unable to create a new source.")
        sys.exit(1)
        
    source["id"] = id
    return source
