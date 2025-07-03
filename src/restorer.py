from sqlite3 import Connection

import os

def restore_directory(conn: Connection, target_path: str, ignores: list):
    ignores.append(".safesync");
    for root, _dirs, files in os.walk(target_path):
        ignored: bool = False
        crnt: list = root.split(os.sep)
        for ignr in ignores:
            if ignr in crnt:
                ignored = True

        if ignored:
            continue
            
        for file in files:
            print(file)
