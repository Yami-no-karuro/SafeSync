import os
from sqlite3 import Connection
from typing import List

from lib.libhash.bindings import fnv1a
from lib.libcompress.bindings import huf_decompress
from src.entities.sources import get_sources
from src.utils.ignore import load_ignores

def should_ignore(path: str, ignores: List[str]) -> bool:
    segments: list = path.split(os.sep)
    return any(ign in segments for ign in ignores)

def restore_directory(conn: Connection, target_path: str, ignore_path: str, target_state_id: int):
    trg_sources: dict = get_sources(conn, target_state_id)
    ignores: list = load_ignores(ignore_path) + [".safesync"]

    for root, _, files in os.walk(target_path):
        if should_ignore(root, ignores):
            continue

        for file in files:
            path: str = os.path.join(root, file)
            restore_file(path, trg_sources)

    for key, source in trg_sources.items():
        huf_decompress(source["obj_path"], source["path"])
        print(f"File \"{source['path']}\" ({source['path_hash']}) successfully restored.")

def restore_file(file_path: str, sources: dict):
    file_path_hash: str = hex(fnv1a(file_path.encode()))[2:]
    if file_path_hash in sources:
        source: dict = sources[file_path_hash]
        huf_decompress(source["obj_path"], source["path"])

        del sources[file_path_hash]
        print(f"File \"{file_path}\" ({file_path_hash}) successfully restored.")
    else:
        os.remove(file_path)
