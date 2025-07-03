from lib.sqlite import sqlite_connect
from src.utils.db import create_sources_table
from src.utils.db import create_states_table
from src.utils.db import spawn_state
from src.scanner import scan_directory

from sqlite3 import Connection

import sys
import os

def init(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    if os.path.exists(root_path):
        print("SafeSync was already initialized.")
        sys.exit(1)

    data_path: str = os.path.join(root_path, "data")
    objects_path: str = os.path.join(root_path, "objects")
    ignore_path: str = os.path.join(dest_path, ".syncignore")

    os.makedirs(data_path)
    os.makedirs(objects_path)

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    create_states_table(conn)
    create_sources_table(conn)
    spawn_state(conn)

    status: dict = scan_directory(conn, objects_path, dest_path, ignore_path)
    
    new: list = status["new"]
    modified: list = status["modified"]
    deleted: list = status["deleted"]
    
    if not new and not modified and not deleted:
        print("No changes detected.")
        conn.close()
        sys.exit(0)
        
    print("===") 
    print(f"New objects: {len(status['new'])}.")
    print(f"Modified objects: {len(status['modified'])}.")
    print(f"Deleted objects: {len(status['deleted'])}.")
    
    conn.close()
