import os
import sys
from sqlite3 import Connection
from typing import List

from lib.libhash.bindings import fnv1a, fnv1a_file
from src.entities.state import fetch_latest_state, add_state
from src.entities.state import fetch_states
from src.entities.sources import spawn_source
from src.entities.sources import fetch_sources_by_state
from src.entities.objects import create_source_object
from src.utils.ignore import load_ignores

def should_ignore(path: str, ignores: List[str]) -> bool:
    segments: list = path.split(os.sep)
    return any(ign in segments for ign in ignores)

def scan_directory(conn: Connection, storage_path: str, target_path: str, ignore_path: str, o_status: bool = False) -> dict:
    lts_state: dict | None = fetch_latest_state(conn)
    if lts_state is None:
        print(f"Unable to fetch latest state.")
        conn.close()
        sys.exit(1)
    
    all_states = fetch_states(conn)
    state_ids = [s["id"] for s in sorted(all_states, key=lambda x: x["id"]) if s["id"] <= lts_state["id"]]
    
    virtual_sources = {}
    removed = set()
    
    for sid in state_ids:
        sources = fetch_sources_by_state(conn, sid)
        if not sources:
            continue
            
        for src in sources.values():
            if src["path_hash"] in removed:
                continue
                
            if src["update_type"] == 2:
                if src["path_hash"] in virtual_sources:
                    del virtual_sources[src["path_hash"]]
                    
                removed.add(src["path_hash"])
                
            elif src["update_type"] == 1:
                virtual_sources[src["path_hash"]] = {
                    "obj_path": src["obj_path"],
                    "path": src["path"],
                    "path_hash": src["path_hash"],
                    "content_hash": src["content_hash"]
                }

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
        crn_state: dict = add_state(conn, lts_state["id"], virtual_sources)

    status["state_id"] = crn_state["id"]
    status["state_time"] = crn_state["time"]

    sources_for_scan = dict(virtual_sources)
    for root, _, files in os.walk(target_path):
        if should_ignore(root, ignores):
            continue

        for file in files:
            status["scanned"] += 1
            path: str = os.path.join(root, file)
            snap_file(conn, path, storage_path, crn_state["id"], sources_for_scan, status, o_status)

    for _, entry in sources_for_scan.items():
        status["deleted"].append((entry["path"], [entry["path_hash"]]))
        if not o_status:
            spawn_source(conn, crn_state["id"], {
                "obj_path": None,
                "path": entry["path"],
                "path_hash": entry["path_hash"],
                "content_hash": None,
                "update_type": 2
            })

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
                print(f"Object file for \"{file_path}\" ({file_path_hash}) successfully created.")
                
                spawn_source(conn, state_id, {
                    "obj_path": obj_path,
                    "path": file_path,
                    "path_hash": file_path_hash,
                    "content_hash": content_hash,
                    "update_type": 1
                })
                
        del sources[file_path_hash]
        
    else:
        status["new"].append((file_path, file_path_hash))
        if not o_status:
            obj_path = create_source_object(storage_path, state_id, file_path, file_path_hash)
            print(f"Object file for \"{file_path}\" ({file_path_hash}) successfully created.")
            
            spawn_source(conn, state_id, {
                "obj_path": obj_path,
                "path": file_path,
                "path_hash": file_path_hash,
                "content_hash": content_hash,
                "update_type": 1
            })
