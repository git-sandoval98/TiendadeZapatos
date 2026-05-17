import sqlite3
import datetime
from werkzeug.security import generate_password_hash
from config import SQLITE_DB


def get_db():
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT NOT NULL,
            apellido        TEXT NOT NULL,
            email           TEXT NOT NULL UNIQUE,
            password_hash   TEXT NOT NULL,
            rol             TEXT NOT NULL DEFAULT 'usuario'
                            CHECK(rol IN ('administrador', 'usuario')),
            activo          INTEGER NOT NULL DEFAULT 1,
            fecha_registro  DATETIME DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso   DATETIME
        );

        CREATE TABLE IF NOT EXISTS sesiones_chat (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id      INTEGER NOT NULL,
            rol_mensaje     TEXT NOT NULL CHECK(rol_mensaje IN ('user', 'assistant')),
            contenido       TEXT NOT NULL,
            modelo_ia       TEXT DEFAULT 'meta-llama/llama-3.3-70b-instruct:free',
            fecha           DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
        CREATE INDEX IF NOT EXISTS idx_chat_usuario ON sesiones_chat(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_chat_fecha ON sesiones_chat(fecha);
    """)

    existing = cursor.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        ("admin@zapatosstore.com",)
    ).fetchone()

    if not existing:
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, email, password_hash, rol) VALUES (?, ?, ?, ?, ?)",
            ("Admin", "ZapatosStore", "admin@zapatosstore.com",
             generate_password_hash("admin123"), "administrador")
        )

    conn.commit()
    conn.close()


# --- CRUD Usuarios ---

def obtener_usuario_por_email(email):
    db = get_db()
    user = db.execute("SELECT * FROM usuarios WHERE email = ? AND activo = 1", (email,)).fetchone()
    db.close()
    return user


def obtener_usuario_por_id(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return user


def crear_usuario(nombre, apellido, email, password_hash, rol="usuario"):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO usuarios (nombre, apellido, email, password_hash, rol) VALUES (?, ?, ?, ?, ?)",
            (nombre, apellido, email, password_hash, rol)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()


def listar_usuarios():
    db = get_db()
    users = db.execute(
        "SELECT id, nombre, apellido, email, rol, activo, fecha_registro, ultimo_acceso FROM usuarios ORDER BY fecha_registro DESC"
    ).fetchall()
    db.close()
    return users


def actualizar_ultimo_acceso(user_id):
    db = get_db()
    db.execute(
        "UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?",
        (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id)
    )
    db.commit()
    db.close()


# --- CRUD Sesiones Chat ---

def guardar_mensaje_chat(usuario_id, rol_mensaje, contenido):
    db = get_db()
    db.execute(
        "INSERT INTO sesiones_chat (usuario_id, rol_mensaje, contenido) VALUES (?, ?, ?)",
        (usuario_id, rol_mensaje, contenido)
    )
    db.commit()
    db.close()


def obtener_historial_chat(usuario_id, limite=20):
    db = get_db()
    mensajes = db.execute(
        "SELECT rol_mensaje, contenido, fecha FROM sesiones_chat WHERE usuario_id = ? ORDER BY fecha DESC LIMIT ?",
        (usuario_id, limite)
    ).fetchall()
    db.close()
    return list(reversed(mensajes))


def limpiar_historial_chat(usuario_id):
    db = get_db()
    db.execute("DELETE FROM sesiones_chat WHERE usuario_id = ?", (usuario_id,))
    db.commit()
    db.close()
