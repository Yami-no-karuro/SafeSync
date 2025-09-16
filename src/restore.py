import os
from sqlite3 import Connection
from typing import List

from lib.libcompress.bindings import huf_decompress
from src.utils.ignore import load_ignores
from src.entities.state import fetch_states
from src.entities.sources import fetch_sources_by_state

def should_ignore(path: str, ignores: list) -> bool:
    return any(ign in path for ign in ignores)
    
def get_state_ids(states: list, max_id: int) -> list:
    sorted_states: list = sorted(states, key = lambda s: s["id"], reverse = True)
    filtered_ids: list = []
    
    for s in sorted_states:
        if s["id"] <= max_id:
            filtered_ids.append(s["id"])
            
    return filtered_ids

def restore_directory(conn: Connection, target_path: str, ignore_path: str, target_state_id: int):
    ignores: list = load_ignores(ignore_path) + [".safesync"]
    all_states: list = fetch_states(conn)
    state_ids: list = get_state_ids(all_states, target_state_id)

    file_map = {}
    removed = set()

    for sid in state_ids:
        sources: dict | None = fetch_sources_by_state(conn, sid)
        if sources is None:
            continue
            
        for src in sources.values():
            if src["path_hash"] in file_map or src["path_hash"] in removed:
                continue
                
            if src["update_type"] == 2:
                removed.add(src["path_hash"])
                
            elif src["update_type"] == 1:
                file_map[src["path_hash"]] = {
                    "obj_path": src["obj_path"],
                    "path": src["path"],
                    "content_hash": src["content_hash"]
                }

    restored_paths = set()
    for src in file_map.values():
        
        try:
            huf_decompress(src["obj_path"], src["path"])
        except Exception as e:
            print(f"An unexpected error occurred during the execution of \"huf_decompress\" on file {src['obj_path']}: {e}")
            continue
        
        print(f"File \"{src['path']}\" successfully restored.")
        restored_paths.add(os.path.abspath(src["path"]))

    for root, _, files in os.walk(target_path):
        if should_ignore(root, ignores):
            continue

        for file in files:
            path = os.path.abspath(os.path.join(root, file))
            if path not in restored_paths:
                os.remove(path)
                print(f"File \"{path}\" successfully deleted (not present in target state).")
