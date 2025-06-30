from lib.sqlite import sqlite_connect

from src.db import create_sources_table
from src.db import create_states_table
from src.snap import snap_directory

from sqlite3 import Connection

import sys
import os

def init(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    if os.path.exists(root_path):
        print("SafeSync was already initialized.")
        print("Exiting...")
        sys.exit(1)

    data_path: str = os.path.join(root_path, "data")
    objects_path: str = os.path.join(root_path, "objects")

    os.makedirs(data_path)
    os.makedirs(objects_path)

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    create_states_table(conn)
    create_sources_table(conn)

    snap_directory(conn, objects_path, dest_path)
    conn.close()
