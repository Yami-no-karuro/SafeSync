from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_fetchone
from lib.sqlite import sqlite_fetchall

from src.db import add_state
from src.db import add_source

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

def status_dir(conn: Connection, dir_path: str):
    state: int | None = sqlite_fetchone(conn, "SELECT MAX(id) FROM states;")[0]
    if state is None:
        print("Unable to fetch the latest state.")
        print("Exiting...")
        sys.exit(1)

    sources: list[tuple] | None = sqlite_fetchall(conn, """
        SELECT * FROM sources
        WHERE state = ?
    """, (state,))
    if sources is None:
        print("Unable to fetch the latest state.")
        print("Exiting...")
        sys.exit(1)

    sources_dict: dict = {}
    for source in sources:
        sources_dict[source[3]] = {
            "id": source[0],
            "state": source[1],
            "path": source[2],
            "path_hash": source[3],
            "content_hash": source[4]
        }

    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            status_file(sources_dict, os.path.join(root, file))

    for remaining in sources_dict:
        print(f"MODIFIED: \"{remaining['path']}\" ({remaining['path_hash']})")

    print(f"Status for directory \"{dir_path}\" completed successfully.")

def status_file(sources: dict, file_path: str):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    content_hash: str = hex(fnv1a_file(file_path))[2:]

    if file_path_hash in sources:
        entry: dict = sources[file_path_hash]
        if entry["content_hash"] != content_hash:
            print(f"MODIFIED: \"{file_path}\" ({file_path_hash})")
    else:
        print(f"NEW: \"{file_path}\" ({file_path_hash})")
        return

    del sources[file_path_hash]
