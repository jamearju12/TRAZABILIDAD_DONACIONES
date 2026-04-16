# Contributing to Trazabilidad de Donaciones de Alimentos

Gracias por tu interés en contribuir a esta entrega parcial de software libre.

## Alcance de esta carpeta

Este repositorio está limitado a la capa de persistencia. Las contribuciones deben mantenerse dentro de estos componentes:

- Conexión a base de datos
- Modelos de dominio
- Repositorios
- Script SQL de esquema y procedimientos almacenados
- Documentación asociada a esta capa

No deben agregarse endpoints HTTP, servicios de aplicación ni interfaces de usuario en esta entrega.

## Cómo contribuir

### Reportar errores

- Describe el problema de forma clara
- Indica el repositorio afectado o el procedimiento almacenado involucrado
- Incluye pasos para reproducirlo
- Indica versión de Python, motor de base de datos y driver ODBC

### Sugerir mejoras

- Explica la mejora propuesta
- Justifica su impacto en mantenimiento, trazabilidad o integridad de datos
- Aclara si el cambio afecta repositorios, modelos o SQL

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
- Documenta cualquier cambio relevante en SQL o comportamiento transaccional
- Evita incluir credenciales reales en archivos versionados

## Licencia

Al contribuir, aceptas que tu código será licenciado bajo LGPL-2.1-or-later como el resto del proyecto.
