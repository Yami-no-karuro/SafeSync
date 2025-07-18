from lib.sqlite import sqlite_connect
from src.entities.state import get_state
from src.entities.state import get_latest_state
from src.restore import restore_directory

from sqlite3 import Connection

import sys
import os

def restore(dest_path: str, trg_state_id: int):
    root_path: str = os.path.join(dest_path, ".safesync")
    if not os.path.exists(root_path):
        print("Not a SafeSync repository.")
        sys.exit(1)

    ignore_path: str = os.path.join(dest_path, ".syncignore")
    data_path: str = os.path.join(root_path, "data")
    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    lts_state: dict = get_latest_state(conn)
    trg_state: dict | None = get_state(conn, trg_state_id)
    if trg_state is None:
        print(f"Unregistered state: {trg_state_id}.")
        conn.close()
        sys.exit(1)
        
    restore_directory(conn, dest_path, ignore_path, trg_state["id"])
  
    print(f"Previous State: {lts_state['id']} ({lts_state['time']}).")
    print(f"Roll-back state: {trg_state['id']} ({trg_state['time']}).")
    print(f"Attention! To persist the roll-back state a new snapshot must be executed.")
   
    conn.close()
