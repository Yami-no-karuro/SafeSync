from sqlite3 import Connection

from src.entities.state import get_states
from lib.sqlite import sqlite_connect
from src.utils.path import get_paths

def states(dest_path: str):
    paths: dict = get_paths(dest_path)
    conn: Connection = sqlite_connect(paths["db_path"])
    
    states: list = get_states(conn)
    print(f"Available states: {len(states)}.")
    for entry in states:
        print(f" - {entry['id']} ({entry['time']})")
        
    conn.close()
