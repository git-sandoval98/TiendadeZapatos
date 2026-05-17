-- ZapatosStore - Script SQL de referencia
-- Este script se ejecuta automaticamente via database.py

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
