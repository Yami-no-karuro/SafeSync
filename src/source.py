from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from src.db import add_state
from src.db import add_source
from src.db import get_latest_state
from src.db import get_sources_by_state

from sqlite3 import Connection

import sys
import os

def source_dir(conn: Connection, dir_path: str):
    state: int | None = add_state(conn)
    if state is None:
        print("Unable to fetch the latest state.")
        print("Exiting...")
        sys.exit(1)

    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            source_file(conn, state, os.path.join(root, file))

    print(f"Directory \"{dir_path}\" successfully sourced.")

def source_file(conn: Connection, state: int, file_path: str):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    source: dict = {
        "path": file_path,
        "path_hash": file_path_hash,
        "content_hash": content_hash
    }

    add_source(conn, state, source)
    print(f"File: \"{file_path}\" ({file_path_hash}) successfully sourced.")

def status_dir(conn: Connection, dir_path: str) -> dict:
    state: int | None = get_latest_state(conn)
    if state is None:
        print("Unable to fetch the latest state.")
        print("Exiting...")
        sys.exit(1)

    sources: dict | None = get_sources_by_state(conn, state)
    if sources is None:
        sources = {}

    new: list = []
    modified: list = []
    deleted: list = []

    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            status_file(sources, os.path.join(root, file), new, modified)

    for remaining in sources:
        entry: dict = sources[remaining]
        deleted.append((entry["path"], [entry["path_hash"]]))
        print(f"DELETED: \"{entry['path']}\" ({entry['path_hash']})")

    return {
        "new": new,
        "modified": modified,
        "deleted": deleted
    }

def status_file(sources: dict, file_path: str, new: list, modified: list):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    if file_path_hash in sources:
        entry: dict = sources[file_path_hash]
        if entry["content_hash"] != content_hash:
            modified.append((file_path, file_path_hash))
            print(f"MODIFIED: \"{file_path}\" ({file_path_hash})")
    else:
        new.append((file_path, file_path_hash))
        print(f"NEW: \"{file_path}\" ({file_path_hash})")
        return

    del sources[file_path_hash]
