"""
setup_admin.py — Genera el hash bcrypt de la contraseña administradora
y lo actualiza en la tabla `usuarios`.

Ejecutar una sola vez después de cargar trazabilidad_alimentos.sql:

    python3 setup_admin.py

Se puede usar también para crear usuarios adicionales o cambiar contraseñas.
"""

import getpass
import os
import sys

import bcrypt

from dotenv import load_dotenv

from database_trazabilidad import DatabaseTrazabilidad


load_dotenv()


def _prompt_password(prompt: str) -> str:
    password = getpass.getpass(prompt)
    confirm = getpass.getpass("Confirmar contraseña: ")
    if password != confirm:
        print("ERROR: Las contraseñas no coinciden.", file=sys.stderr)
        sys.exit(1)
    if len(password) < 8:
        print("ERROR: La contraseña debe tener al menos 8 caracteres.", file=sys.stderr)
        sys.exit(1)
    return password


def set_password(email: str, password: str) -> bool:
    """Actualiza el hash bcrypt de un usuario identificado por email."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    connection = DatabaseTrazabilidad().get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE usuarios SET password_hash = ? WHERE email = ?",
            hashed,
            email,
        )
        rows = cursor.rowcount
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return rows > 0


def create_user(nombre: str, email: str, password: str, rol_nombre: str = "ADMIN") -> int | None:
    """Crea un nuevo usuario con contraseña hasheada. Retorna el id o None."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    connection = DatabaseTrazabilidad().get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM roles WHERE nombre = ?", rol_nombre)
        row = cursor.fetchone()
        if not row:
            print(f"ERROR: Rol '{rol_nombre}' no existe.", file=sys.stderr)
            return None

        rol_id = row.id
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol_id, activo, fecha_creacion) "
            "VALUES (?, ?, ?, ?, 1, NOW())",
            nombre,
            email,
            hashed,
            rol_id,
        )
        connection.commit()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", email)
        new_row = cursor.fetchone()
        return new_row.id if new_row else None
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("=== Configuración de contraseña de administrador ===\n")
    email = "admin@trazabilidad.local"

    print(f"Configurando contraseña para: {email}")
    password = _prompt_password("Nueva contraseña: ")

    actualizado = set_password(email, password)
    if actualizado:
        print(f"\nContraseña actualizada correctamente para {email}.")
    else:
        print(
            f"\nEl usuario {email} no existe. Creándolo ahora...",
        )
        nombre = input("Nombre completo del admin: ").strip() or "Usuario Admin"
        nuevo_id = create_user(nombre, email, password, "ADMIN")
        if nuevo_id:
            print(f"Usuario admin creado con ID: {nuevo_id}")
        else:
            print("ERROR: No se pudo crear el usuario admin.", file=sys.stderr)
            sys.exit(1)

    print("\nEjecuta ahora: python3 api_trazabilidad.py")
