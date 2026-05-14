# Contributing to Trazabilidad de Donaciones de Alimentos

Gracias por tu interés en contribuir a esta entrega parcial de software libre.

## Alcance de este repositorio

Este repositorio incluye la capa de persistencia completa más la API REST con autenticación. Las contribuciones deben mantenerse dentro de estos componentes:

- Conexión a base de datos
- Modelos de dominio
- Repositorios
- Script SQL de esquema y procedimientos almacenados
- API REST Flask (`api_trazabilidad.py`)
- Módulo de autenticación JWT y bcrypt (`auth_trazabilidad.py`)
- Documentación asociada

## Cómo contribuir

### Reportar errores

- Describe el problema de forma clara
- Indica el repositorio afectado o el procedimiento almacenado involucrado
- Incluye pasos para reproducirlo
- Indica versión de Python, motor de base de datos y driver ODBC

### Sugerir mejoras

- Explica la mejora propuesta
- Justifica su impacto en mantenimiento, trazabilidad, seguridad o integridad de datos
- Aclara si el cambio afecta repositorios, modelos, SQL, endpoints o autenticación

### Enviar cambios de código

1. Haz fork del repositorio.
2. Crea una rama para tu cambio: `git checkout -b feature/nombre-cambio`
3. Realiza commits pequeños y descriptivos.
4. Publica tu rama en GitHub.
5. Abre un Pull Request con explicación técnica del cambio.

## Estándares de código

- Usa Python 3.8 o superior
- Sigue PEP 8
- Mantén los repositorios enfocados en acceso a datos
- Los endpoints nuevos deben estar decorados con `@requiere_jwt`
- Las contraseñas deben manejarse únicamente con bcrypt (nunca en texto plano)
- No expongas el `JWT_SECRET_KEY` ni credenciales en el código
- Documenta cualquier cambio relevante en SQL, endpoints o comportamiento transaccional
- Evita incluir credenciales reales en archivos versionados

## Licencia

Al contribuir, aceptas que tu código será licenciado bajo LGPL-2.1-or-later como el resto del proyecto.
