from sqlite3 import Connection
import sqlite3

def sqlite_connect(db_file: str) -> Connection:
    return sqlite3.connect(db_file)

def sqlite_execute(conn: Connection, query: str, params: tuple = ()) -> int | None:
    with conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid

def sqlite_fetchone(conn: Connection, query: str, params: tuple = ()) -> tuple:
    cursor = conn.cursor()
    cursor.execute(query, params)

    return cursor.fetchone()

def sqlite_fetchall(conn: Connection, query: str, params: tuple = ()) -> list[tuple]:
    cursor = conn.cursor()
    cursor.execute(query, params)

    return cursor.fetchall()
