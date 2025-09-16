import sys
from sqlite3 import Connection

from lib.sqlite import sqlite_connect
from src.entities.state import fetch_state_by_id
from src.entities.state import fetch_latest_state
from src.restore import restore_directory
from src.utils.path import get_paths

def restore(dest_path: str, trg_state_id: int):
    paths: dict = get_paths(dest_path)
    conn: Connection = sqlite_connect(paths["db_path"])

    lts_state: dict | None = fetch_latest_state(conn)
    if lts_state is None:
        print(f"Unable to fetch latest state.")
        conn.close()
        sys.exit(1)
        
    trg_state: dict | None = fetch_state_by_id(conn, trg_state_id)
    if trg_state is None:
        print(f"Unregistered state: {trg_state_id}.")
        conn.close()
        sys.exit(1)
        
    restore_directory(conn, 
        paths["dest_path"], 
        paths["ignore_path"], 
        trg_state["id"]
    )
  
    print(f"Previous State: {lts_state['id']} ({lts_state['time']}).")
    print(f"Roll-back state: {trg_state['id']} ({trg_state['time']}).")
    print(f"Attention! To persist the roll-back state a new snapshot must be executed.")
   
    conn.close()
