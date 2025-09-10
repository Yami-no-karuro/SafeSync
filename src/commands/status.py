from lib.sqlite import sqlite_connect
from src.scan import scan_directory
from src.utils.path import get_paths

from sqlite3 import Connection
from sys import exit as sys_exit

def status(dest_path: str):
    paths: dict = get_paths(dest_path)
    conn: Connection = sqlite_connect(paths["db_path"])
    
    status: dict = scan_directory(
        conn, 
        paths["objects_path"], 
        paths["dest_path"], 
        paths["ignore_path"], 
        True
    )
    
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
        sys_exit(0)
       
    print("===") 
    print(f"New objects: {len(status['new'])}.")
    print(f"Modified objects: {len(status['modified'])}.")
    print(f"Deleted objects: {len(status['deleted'])}.")

    conn.close()
