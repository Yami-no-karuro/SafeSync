import os
from sqlite3 import Connection
from typing import List

from lib.libhash.bindings import fnv1a, fnv1a_file
from src.entities.state import get_latest_state, add_state
from src.entities.sources import get_sources, add_source
from src.entities.objects import create_source_object
from src.utils.ignore import load_ignores

def should_ignore(path: str, ignores: List[str]) -> bool:
    segments: list = path.split(os.sep)
    return any(ign in segments for ign in ignores)

def scan_directory(conn: Connection, storage_path: str, target_path: str, ignore_path: str, o_status: bool = False) -> dict:
    lts_state: dict = get_latest_state(conn)
    lts_sources: dict = get_sources(conn, lts_state["id"])

    ignores: list = load_ignores(ignore_path) + [".safesync"]
    status: dict = {
        "state_id": None,
        "state_time": None,
        "scanned": 0,
        "new": [],
        "modified": [],
        "deleted": []
    }
   
    crn_state: dict = lts_state
    if not o_status:
        crn_state: dict = add_state(conn, lts_state["id"], lts_sources)
        
    status["state_id"] = crn_state["id"]
    status["state_time"] = crn_state["time"]

    for root, _, files in os.walk(target_path):
        if should_ignore(root, ignores):
            continue

        for file in files:
            status["scanned"] += 1
            path: str = os.path.join(root, file)
            snap_file(conn, path, storage_path, crn_state["id"], lts_sources, status, o_status)

    for _, entry in lts_sources.items():
        status["deleted"].append((entry["path"], [entry["path_hash"]]))

    return status

def snap_file(conn: Connection, file_path: str, storage_path: str, state_id: int, sources: dict, status: dict, o_status: bool = False):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    obj_path: str | None = None
    if file_path_hash in sources:
        source: dict = sources[file_path_hash]

        if source["content_hash"] != content_hash:
            status["modified"].append((file_path, file_path_hash))
            if not o_status:
                obj_path = create_source_object(storage_path, state_id, file_path, file_path_hash)
                print(f"Object \"{obj_path}\" successfully added.")
        else:
            if not o_status:
                obj_path = source["obj_path"]

        del sources[file_path_hash]
    else:
        status["new"].append((file_path, file_path_hash))
        if not o_status:
            obj_path = create_source_object(storage_path, state_id, file_path, file_path_hash)
            print(f"Object \"{obj_path}\" successfully added.")

    if not o_status:
        add_source(conn, state_id, {
            "obj_path": obj_path,
            "path": file_path,
            "path_hash": file_path_hash,
            "content_hash": content_hash
        })
