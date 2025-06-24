from lib.libhash.bindings import fnv1a
from lib.libhash.bindings import fnv1a_file

from lib.sqlite import sqlite_connect
from lib.sqlite import sqlite_execute
from lib.sqlite import sqlite_fetchone

from datetime import datetime
from sqlite3 import Connection

import os
import json

def init(destination: str):
    db_path: str = f"{destination}/.safesync/data/db/safesync-core.db"

    init_root(destination)
    init_metadata(destination)
    init_db(db_path)
    source_dir(destination, db_path)

def init_root(path: str):
    root: str = f"{path}/.safesync"

    db_dir: str = os.path.join(root, 'data', 'db')
    objects_dir: str = os.path.join(root, 'data', 'objects')
    os.makedirs(db_dir, exist_ok = True)
    os.makedirs(objects_dir, exist_ok = True)

def init_metadata(path: str):
    metadata_path: str = os.path.join(path, '.safesync', 'metadata.json')
    metadata: dict = {
        "time": datetime.now().timestamp(),
        "source": path,
        "root": f"{path}/.safesync"
    }

    with open(metadata_path, 'w') as json_file:
        json.dump(metadata, json_file, indent = 4)

    print(f"File \"{metadata_path}\" successfully created.")

def init_db(db_path: str):
    conn: Connection = sqlite_connect(db_path)
    try:
        sqlite_execute(conn, """
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                filepath_hash TEXT NOT NULL,
                hash TEXT NOT NULL
            );
        """)

        print("Table \"sources\" successfully created.")
    except Exception as e:
        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
    finally:
        conn.close()

def source_dir(dir_path: str, db_path: str):
    conn: Connection = sqlite_connect(db_path)
    try:
        for root, _dirs, files in os.walk(dir_path):
            for file in files:
                source_file(root, file, conn)

        print(f"Directory \"{dir_path}\" successfully sourced.")
    except Exception as e:
        print(f"An unexpected error occurred: \"{e}\"")
        print("Exiting...")
    finally:
        conn.close()

def source_file(root: str, file: str, conn: Connection):
    filepath: str = os.path.join(root, file)
    filepath_hash: int = fnv1a(b"{filepath}")
    hash: int = fnv1a_file(filepath)

    query: str = """
        SELECT * FROM sources
        WHERE filepath = ?;
    """

    entry: tuple | None = sqlite_fetchone(conn, query, (filepath,))
    if entry is not None:
        print(f"Skipping entry, file: \"{filepath}\" was already added to the sources index.")
        return

    filepath_hash_hex: str = hex(filepath_hash)[2:]
    hash_hex: str = hex(hash)[2:]

    query: str = """
        INSERT INTO sources (
            filepath,
            filepath_hash,
            hash
        ) VALUES (?, ?, ?);
    """

    sqlite_execute(conn, query, (filepath, filepath_hash_hex, hash_hex))
    print(f"File \"{filepath}\" successfully added to the sources index.")
