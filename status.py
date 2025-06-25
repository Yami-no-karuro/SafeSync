from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_connect, sqlite_fetchone

from src.db import create_sources_table
from src.db import create_states_table
from src.source import source_dir, status_dir

from sqlite3 import Connection

import os

def status(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    data_path: str = os.path.join(root_path, "data")
    objects_path: str = os.path.join(root_path, "objects")

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    status_dir(conn, dest_path)
    conn.close()
