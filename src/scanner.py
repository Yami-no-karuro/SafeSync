from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from src.entities.state import get_latest_state
from src.entities.state import add_state

from src.entities.sources import get_latest_sources
from src.entities.sources import add_source

from src.entities.objects import create_source_object

from sqlite3 import Connection

import os

def scan_directory(conn: Connection, storage_path: str, target_path: str, o_status: bool = False) -> dict:
    lts_state: int = get_latest_state(conn)
    lts_sources: dict = get_latest_sources(conn, lts_state)

    status: dict = {
        "state": None,
        "scanned": 0,
        "new": [],
        "modified": [],
        "deleted": []
    }

    crn_state: int = lts_state
    if o_status is False:
        crn_state: int = add_state(conn, lts_state, lts_sources)
        
    status["state"] = crn_state

    for root, _dirs, files in os.walk(target_path):
        if ".safesync" in root.split(os.sep):
            continue

        for file in files:
            status["scanned"] += 1
            path: str = os.path.join(root, file)
            snap_file(conn, storage_path, crn_state, lts_sources, path, status, o_status)

    for key in lts_sources:
        entry: dict = lts_sources[key]
        status["deleted"].append((entry["path"], [entry["path_hash"]]))

    return status

def snap_file(conn: Connection, storage_path: str, state: int, sources: dict, file_path: str, status: dict, o_status: bool = False):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    obj_path: str | None = None
    if file_path_hash in sources:
        source: dict = sources[file_path_hash]
        if source["content_hash"] != content_hash:
            status["modified"].append((file_path, file_path_hash))
            if o_status is False:
                obj_path = create_source_object(storage_path, state, file_path, file_path_hash)
                print(f"Object \"{obj_path}\" successfully added.")
        else:
            if o_status is False:
                obj_path = source["obj_path"]

        del sources[file_path_hash]
    else:
        status["new"].append((file_path, file_path_hash))
        if o_status is False:
            obj_path = create_source_object(storage_path, state, file_path, file_path_hash)
            print(f"Object \"{obj_path}\" successfully added.")

    if o_status is False:
        add_source(conn, state, {
            "obj_path": obj_path,
            "path": file_path,
            "path_hash": file_path_hash,
            "content_hash": content_hash
        })
