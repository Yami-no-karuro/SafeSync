import sys
from sqlite3 import Connection

from lib.sqlite import sqlite_connect
from src.scan import scan_directory
from src.utils.path import get_paths

def snap(dest_path: str):
    paths: dict = get_paths(dest_path)
    conn: Connection = sqlite_connect(paths["db_path"])

    status: dict = scan_directory(
        conn, 
        paths["objects_path"], 
        paths["dest_path"], 
        paths["ignore_path"]
    )
    
    new: list = status["new"]
    modified: list = status["modified"]
    deleted: list = status["deleted"]
    
    if not new and not modified and not deleted:
        print("No changes detected.")
        conn.close()
        sys.exit(0)
        
    print("===") 
    print(f"New objects: {len(status['new'])}.")
    print(f"Modified objects: {len(status['modified'])}.")
    print(f"Deleted objects: {len(status['deleted'])}.")
    
    conn.close()
