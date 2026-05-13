import os
import datetime
import functools

import flask
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from database_trazabilidad import DatabaseTrazabilidad


load_dotenv()

# Contexto de hashing: bcrypt con factor de costo 12 (OWASP recomendado)
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


# ---------------------------------------------------------------------------
# Utilidades de contraseña
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica una contraseña en texto plano contra su hash bcrypt."""
    return _pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# Utilidades JWT
# ---------------------------------------------------------------------------

def _get_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret or len(secret) < 32:
        raise RuntimeError(
            "JWT_SECRET_KEY no definida o demasiado corta en .env (mínimo 32 caracteres)"
        )
    return secret


def create_token(usuario_id: int, email: str, rol: str) -> str:
    """Genera un JWT firmado con HS256 para el usuario autenticado."""
    expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "8"))
    now = datetime.datetime.utcnow()
    payload = {
        "sub": str(usuario_id),
        "email": email,
        "rol": rol,
        "iat": now,
        "exp": now + datetime.timedelta(hours=expiration_hours),
    }
    return jwt.encode(payload, _get_secret(), algorithm="HS256")


def decode_token(token: str) -> dict:
    """Decodifica y valida un JWT. Lanza ValueError si es inválido o expirado."""
    try:
        return jwt.decode(token, _get_secret(), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")


# ---------------------------------------------------------------------------
# Verificación de credenciales contra la base de datos
# ---------------------------------------------------------------------------

def verificar_credenciales(email: str, password: str) -> dict | None:
    """
    Busca al usuario por email en la tabla `usuarios` (activo=1) y
    verifica la contraseña contra el hash bcrypt almacenado en `password_hash`.

    Retorna un dict con {id, nombre, email, rol} si las credenciales son
    correctas, o None en caso contrario.

    Nota: la columna `password_hash` debe existir en la tabla `usuarios`.
    Ejecutar la migración incluida en trazabilidad_alimentos.sql antes de usar.
    """
    connection = DatabaseTrazabilidad().get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT u.id, u.nombre, u.email, u.password_hash, r.nombre AS rol "
            "FROM usuarios u "
            "INNER JOIN roles r ON r.id = u.rol_id "
            "WHERE u.email = ? AND u.activo = 1",
            email,
        )
        row = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if not row:
        return None

    if not verify_password(password, row.password_hash):
        return None

    return {
        "id": row.id,
        "nombre": row.nombre,
        "email": row.email,
        "rol": row.rol,
    }


# ---------------------------------------------------------------------------
# Decorador de protección JWT para rutas Flask
# ---------------------------------------------------------------------------

def requiere_jwt(f):
    """
    Decorador Flask que valida el Bearer JWT en el header Authorization.
    Si el token es válido, almacena el payload en flask.g.jwt_payload.
    Responde 401 si el token falta o es inválido.
    """
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = flask.request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return flask.jsonify({
                "estado": "ERROR",
                "mensaje": "Token de autorizacion requerido"
            }), 401

        token = auth_header[len("Bearer "):]
        try:
            flask.g.jwt_payload = decode_token(token)
        except ValueError as exc:
            return flask.jsonify({
                "estado": "ERROR",
                "mensaje": str(exc)
            }), 401

        return f(*args, **kwargs)

    return decorated
