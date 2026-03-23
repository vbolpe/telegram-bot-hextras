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

def user_exists(telegram_id: int) -> str:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def user_name(telegram_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT nombre FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def create_user(telegram_id, legajo, nombre, area, jornada):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, legajo, nombre, area, jornada)
        VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, legajo, nombre, area, jornada))
    conn.commit()
    conn.close()

def overtime_works(telegram_id: int, fecha: str, hora_inicio: str, hora_fin: str,
                   descripcion: str, ticket: str, cliente: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO overtime (telegram_id, fecha, hora_inicio, hora_fin,
                              descripcion, ticket, cliente)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (telegram_id, fecha, hora_inicio, hora_fin,
          descripcion, ticket, cliente))
    conn.commit()
    conn.close()

def workend(telegram_id: int, mes: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT fecha FROM overtime
        WHERE telegram_id = ? AND fecha = ?
        ORDER BY id DESC LIMIT 30
    """, (telegram_id, mes))
    result = cur.fetchone()
    conn.close()
    return result is not None and result[0] is not None

def get_clientes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT nombre FROM clientes ORDER BY nombre")
    rows = cur.fetchall()

    conn.close()
    return [row[0] for row in rows]

def get_overtime_by_moth(telegram_id: int, year: int, month: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                
        SELECT fecha, hora_inicio, hora_fin, description, ticket, cliente FROM overtime WHERE telegram_id = ?
        
        """, (telegram_id,))
    
    rows = cur.fetchall()
    conn.close()

    resultados = []

    for row in rows:
        fecha_str = row[0]
        fecha = datetime.strptime(fecha_str, "%d%m%Y")

        if fecha.year == year and fecha.month == month:
            resultados.append(row)

    return resultados