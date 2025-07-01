from lib.libcompress.bindings import huf_decompress

from src.entities.state import add_state, get_state
from src.entities.state import get_latest_state

from src.entities.sources import get_sources

from lib.sqlite import sqlite_connect

from src.utils.db import create_sources_table
from src.utils.db import create_states_table

from sqlite3 import Connection

import sys
import os

def restore(dest_path: str, trg_state_id: int):
    root_path: str = os.path.join(dest_path, ".safesync")
    if not os.path.exists(root_path):
        print("Not a SafeSync repository.")
        sys.exit(1)

    data_path: str = os.path.join(root_path, "data")
    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    lts_state: dict = get_latest_state(conn)
    trg_state: dict | None = get_state(conn, trg_state_id)
    if trg_state is None:
        print(f"Unregistered state: {trg_state}.")
        conn.close()
        sys.exit(1)
        
    trg_sources: dict = get_sources(conn, trg_state["id"])
    for key in trg_sources:
        trg_source: dict = trg_sources[key]
        huf_decompress(trg_source["obj_path"], trg_source["path"])
        print(f"Object \"{trg_source['obj_path']}\" successfully restored.")
  
    print(f"Previous State: {lts_state['id']} ({lts_state['time']}).")
    print(f"Roll-back state: {trg_state['id']} ({trg_state['time']}).") 
    print(f"Please, remember to take a snapshot to persist the roll-back state.")
   
    conn.close()
