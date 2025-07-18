from lib.sqlite import sqlite_connect
from src.scan import scan_directory

from sqlite3 import Connection

import sys
import os

def status(dest_path: str):
    root_path: str = os.path.join(dest_path, ".safesync")
    if not os.path.exists(root_path):
        print("Not a SafeSync repository.")
        sys.exit(1)

    data_path: str = os.path.join(root_path, "data")
    objects_path: str = os.path.join(root_path, "objects")
    ignore_path: str = os.path.join(dest_path, ".syncignore")

    db_path: str = os.path.join(data_path, "safesync-core.db")
    conn: Connection = sqlite_connect(db_path)
    
    status: dict = scan_directory(conn, objects_path, dest_path, ignore_path, True)
    
    print(f"State: {status['state_id']} ({status['state_time']}).")
    print(f"Scanned objects: {status['scanned']}.")
    print("===")

    new: list = status["new"]
    for source in new:
        print(f"NEW: \"{source[0]}\" ({source[1]}).")

    modified: list = status["modified"]
    for source in modified:
        print(f"MODIFIED: \"{source[0]}\" ({source[1]}).")

    deleted: list = status["deleted"]
    for source in deleted:
        print(f"DELETED: \"{source[0]}\" ({source[1]}).")

    if not new and not modified and not deleted:
        print("No changes detected.")
        conn.close()
        sys.exit(0)
       
    print("===") 
    print(f"New objects: {len(status['new'])}.")
    print(f"Modified objects: {len(status['modified'])}.")
    print(f"Deleted objects: {len(status['deleted'])}.")

    conn.close()
