import sqlite3
import numpy as np


def setup_database():
    conn = sqlite3.connect('security_system.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        barcode TEXT UNIQUE,
                        face_encoding BLOB
                     )''')
    conn.commit()
    return conn

def add_user(conn, barcode, face_encoding):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (barcode, face_encoding) VALUES (?, ?)",
                       (barcode, face_encoding.tobytes()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def remove_user(conn, barcode):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE barcode = ?", (barcode,))
    conn.commit()
    return cursor.rowcount > 0

def fetch_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT barcode FROM users")
    users = cursor.fetchall()

    return [user[0] for user in users]


def validate_barcode(conn, barcode):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE barcode = ?", (barcode,))
    return cursor.fetchone()
