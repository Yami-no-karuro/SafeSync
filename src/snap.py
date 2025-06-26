from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from src.db import add_state
from src.db import add_source
from src.db import get_latest_state
from src.db import get_sources_by_state

from sqlite3 import Connection

import shutil
import sys
import os

def fetch_latest_state(conn: Connection) -> int:
    state: int | None = get_latest_state(conn)
    if state is None:
        print("Unable to fetch the latest state.")
        print("Exiting...")
        sys.exit(1)

    return state

def fetch_new_state(conn: Connection, lts_state: int, lts_sources: dict) -> int:
    state: int | None = None
    if lts_state == 1 and not lts_sources:
        state = lts_state
    else:
        state = add_state(conn)
        if state is None:
            print("Unable to create a new state.")
            print("Exiting...")
            sys.exit(1)

    return state

def fetch_latest_sources(conn: Connection, state: int) -> dict:
    sources: dict | None = get_sources_by_state(conn, state)
    if sources is None:
        sources = {}

    return sources

def add_object(storage_path: str, state: int, file_path: str, file_path_hash: str) -> str:
    obj_dir_path: str = os.path.join(storage_path, f"{state}")
    obj_path: str = os.path.join(obj_dir_path, file_path_hash)

    os.makedirs(obj_dir_path, exist_ok = True)
    shutil.copy(file_path, obj_path)

    return obj_path

def snap_directory(conn: Connection, storage_path: str, target_path: str, status_only: bool = False) -> dict:
    lts_state: int = fetch_latest_state(conn)
    lts_sources: dict = fetch_latest_sources(conn, lts_state)

    status: dict = {
        "new": [],
        "modified": [],
        "deleted": []
    }

    crn_state: int = lts_state
    if status_only is False:
        crn_state: int = fetch_new_state(conn, lts_state, lts_sources)

    for root, _dirs, files in os.walk(target_path):
        if ".safesync" in root.split(os.sep):
            continue

        for file in files:
            path: str = os.path.join(root, file)
            snap_file(conn, storage_path, crn_state, lts_sources, path, status, status_only)

    for key in lts_sources:
        entry: dict = lts_sources[key]
        status["deleted"].append((entry["path"], [entry["path_hash"]]))

    return status

def snap_file(conn: Connection, storage_path: str, state: int, sources: dict, file_path: str, status: dict, status_only: bool = False):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    obj_path: str | None = None
    if file_path_hash in sources:
        source: dict = sources[file_path_hash]
        if source["content_hash"] != content_hash:
            status["modified"].append((file_path, file_path_hash))
            if status_only is False:
                obj_path = add_object(storage_path, state, file_path, file_path_hash)
        else:
            if status_only is False:
                obj_path = source["obj_path"]

        del sources[file_path_hash]
    else:
        status["new"].append((file_path, file_path_hash))
        if status_only is False:
            obj_path = add_object(storage_path, state, file_path, file_path_hash)

    if status_only is False:
        add_source(conn, state, {
            "obj_path": obj_path,
            "path": file_path,
            "path_hash": file_path_hash,
            "content_hash": content_hash
        })
