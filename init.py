from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_connect

from src.db import add_state, create_sources_table
from src.db import create_states_table
from src.db import add_source

from datetime import datetime
from sqlite3 import Connection

import os
import sys

def init(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    data_path: str = os.path.join(root_path, "data")
    os.makedirs(data_path)

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    init_db(conn, db_path)
    source_dir(conn, dest_path, db_path)
    conn.close()

def init_db(conn: Connection, db_path: str):
    create_states_table(conn)
    create_sources_table(conn)

def source_dir(conn: Connection, dir_path: str, db_path: str):
    state: int | None = add_state(conn)
    if state is None:
        print("Unable to fetch latest state.")
        print("Exiting...")
        sys.exit(1)

    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            source_file(conn, state, root, file)

    print(f"Directory \"{dir_path}\" successfully sourced.")

def source_file(conn: Connection, state: int, root_path: str, file_path: str):
    path: str = os.path.join(root_path, file_path)
    path_hash: str = hex(fnv1a(path.encode()))[2:]
    hash: str = hex(fnv1a_file(path))[2:]
    add_source(conn, state, path_hash, hash)

    print(f"File: \"{path}\" ({path_hash}) successfully sourced.")
