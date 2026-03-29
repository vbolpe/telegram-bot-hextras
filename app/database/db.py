import sqlite3
from pathlib import Path
from datetime import datetime

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
            legajo INT NOT NULL,
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
            proyecto TEXT,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    """)

    # Tabla de clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ── Usuarios ──────────────────────────────────────────────────────────────────

def user_exists(telegram_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE telegram_id = ?",(telegram_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def get_user_by_telegram_id(telegram_id: int) -> dict | None:
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT legajo, nombre, area, jornada FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"legajo": row[0], "nombre": row[1], "area": row[2], "jornada": row[3]}

def user_name(telegram_id: int) -> str | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM users WHERE telegram_id = ?",(telegram_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def create_user(telegram_id, legajo, nombre, area, jornada):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, legajo, nombre, area, jornada)
        VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, legajo, nombre, area, jornada))
    conn.commit()
    conn.close()

# ── Clientes ──────────────────────────────────────────────────────────────────

def get_clientes() -> list[str]:
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT nombre FROM clientes ORDER BY nombre")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def client_exists(client: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM clientes WHERE nombre = ?",(client,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def create_client(nombre):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (nombre)
        VALUES (?)
    """, (nombre,))
    conn.commit()
    conn.close()

# ── Proyectos ─────────────────────────────────────────────────────────────────

# ── Horas extra ───────────────────────────────────────────────────────────────

def overtime_works(telegram_id: int, fecha: str, hora_inicio: str, hora_fin: str,
                   descripcion: str, ticket: str, cliente: str, proyecto: str = ""):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO overtime
            (telegram_id, fecha, hora_inicio, hora_fin, descripcion, ticket, cliente, proyecto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (telegram_id, fecha, hora_inicio, hora_fin, descripcion, ticket, cliente, proyecto))
    conn.commit()
    conn.close()

def get_overtime_by_moth(telegram_id: int, year: int, month: int) -> list[tuple]:
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT fecha, hora_inicio, hora_fin, descripcion, ticket, cliente, proyecto
        FROM overtime
        WHERE telegram_id = ?
          AND substr(fecha, 7, 4) = ?   -- año  (DD/MM/YYYY)
          AND substr(fecha, 4, 2) = ?   -- mes
        ORDER BY fecha
    """, (telegram_id, str(year), f"{month:02d}"))
    rows = cur.fetchall()
    conn.close()
    return rows