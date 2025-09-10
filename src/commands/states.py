from src.entities.state import get_states
from lib.sqlite import sqlite_connect

from sqlite3 import Connection
from os.path import exists as os_exists
from os.path import join as os_join
from sys import exit as sys_exit

def get_paths(dest_path: str) -> dict:
    paths: dict = {}

    paths["dest_path"] = dest_path
    paths["root_path"] = os_join(dest_path, ".safesync")
    if not os_exists(paths["root_path"]):
        print("Not a SafeSync repository.")
        sys_exit(1)

    paths["data_path"] = os_join(paths["root_path"], "data")
    paths["objects_path"] = os_join(paths["root_path"], "objects")
    paths["ignore_path"] = os_join(paths["dest_path"], ".syncignore")
    paths["db_path"] = os_join(paths["data_path"], "safesync-core.db")

    return paths

def states(dest_path: str):
    paths: dict = get_paths(dest_path)
    conn: Connection = sqlite_connect(paths["db_path"])
    
    states: list = get_states(conn)
    print(f"Available states: {len(states)}.")
    for entry in states:
        print(f" - {entry['id']} ({entry['time']})")
        
    conn.close()
