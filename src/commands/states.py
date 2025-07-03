from src.entities.state import get_states
from lib.sqlite import sqlite_connect

from sqlite3 import Connection

import sys
import os

def states(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    if not os.path.exists(root_path):
        print("Not a SafeSync repository.")
        sys.exit(1)

    data_path: str = os.path.join(root_path, "data")
    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)
    
    states: list = get_states(conn)
    print(f"Available states: {len(states)}.")
    for entry in states:
        print(f" - {entry['id']} ({entry['time']})")
        
    conn.close()
