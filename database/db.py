import sqlite3
from pathlib import Path

DB_PATH = Path("/app/data/db.sqlite3")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cur = conn.cursor()

    # Tabla usuarios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            legajo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            area TEXT NOT NULL,
            jornada TEXT NOT NULL
        )
    """)

    # Tabla horas extra
    cur.execute("""
        CREATE TABLE IF NOT EXISTS overtime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            descripcion TEXT,
            ticket TEXT,
            cliente TEXT,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    """)

    conn.commit()
    conn.close()

def user_exists(telegram_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def create_user(telegram_id, legajo, nombre, area, jornada):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, legajo, nombre, area, jornada)
        VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, legajo, nombre, area, jornada))
    conn.commit()
    conn.close()
