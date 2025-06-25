from lib.sqlite import sqlite_connect

from src.source import status_dir

from sqlite3 import Connection

import os

def snap(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    data_path: str = os.path.join(root_path, "data")
    objects_path: str = os.path.join(root_path, "objects")

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)

    status: dict = status_dir(conn, dest_path)
    print(status)
    conn.close()
