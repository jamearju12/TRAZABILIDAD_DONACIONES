# Trazabilidad de Donaciones de Alimentos

[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1.html)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/downloads/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-blue)](https://www.mysql.com/)

Entrega parcial del sistema de trazabilidad para gestión de donaciones de alimentos. Esta versión llega hasta la capa de acceso a datos: conexión a base de datos, modelos de dominio, repositorios y script SQL.

## Características principales

✅ **Conexión parametrizada** por variables de entorno  
✅ **Modelos de dominio** para donantes, productos, donaciones y entregas  
✅ **Repositorios especializados** para operaciones CRUD y consultas de trazabilidad  
✅ **Stored procedures y consultas SQL** para inventario, lotes y movimientos  
✅ **Soporte de borrado lógico** en donantes para conservar trazabilidad histórica  
✅ **API REST Flask** con 27 endpoints HTTP protegidos  
✅ **Autenticación JWT (HS256)** con expiración configurable  
✅ **Contraseñas hasheadas con bcrypt** (factor de costo 12, estándar OWASP)  

## Especificaciones técnicas

- **Lenguaje**: Python 3.8+
- **Framework API**: Flask 3.0+
- **Base de datos**: MySQL 5.7+ / MariaDB 10.3+
- **Acceso a datos**: pyodbc + patrón Repository + Stored Procedures
- **Autenticación**: PyJWT 2.8+ (HS256)
- **Encriptación**: bcrypt 4.0+ (cost factor 12)
- **Gestión de secretos**: Variables de entorno con python-dotenv
- **Licencia**: LGPL 2.1 o posterior

## Alcance

El proyecto incluye la capa de persistencia completa más la API REST con autenticación:

- Conexión a base de datos
- Definición de modelos
- Implementación de repositorios
- Script de creación de esquema, datos base y procedimientos almacenados
- API REST Flask con autenticación JWT
- Módulo de seguridad con bcrypt y JWT

## Estructura

```
├── main_trazabilidad.py
│   └─ Punto de entrada de la aplicación
├── api_trazabilidad.py
│   └─ Endpoints REST Flask (27 rutas protegidas + /login)
├── auth_trazabilidad.py
│   └─ JWT, bcrypt y decorador @requiere_jwt
├── setup_admin.py
│   └─ Script único para crear/actualizar contraseña del admin
├── database_trazabilidad.py
│   └─ Capa de conexión con gestión segura de credenciales
├── models_trazabilidad.py
│   └─ Modelos de dominio (entidades)
├── *_repository.py
│   └─ Acceso a datos mediante patrón Repository
└── trazabilidad_alimentos.sql
    └─ Script con tablas y procedimientos almacenados
```

## Instalación rápida

### 1. Requisitos previos

- Python 3.8+
- MySQL 5.7+ o MariaDB 10.3+
- pip (gestor de paquetes Python)

### 2. Clonar o descargar

```bash
git clone https://github.com/tu-usuario/trazabilidad-donaciones-repositorios.git
cd trazabilidad-donaciones-repositorios
```

### 3. Crear entorno virtual

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

### 4. Instalar dependencias

**macOS/Linux**

```bash
python3 -m pip install -r requirements.txt
```

**Windows**

```powershell
py -3 -m pip install -r requirements.txt
```

### 5. Configurar base de datos

**macOS/Linux o Git Bash**

```bash
mysql -u root -p < trazabilidad_alimentos.sql
```

**Windows PowerShell**

```powershell
Get-Content .\trazabilidad_alimentos.sql | mysql -u root -p
```

### 6. Configurar secretos

**macOS/Linux**

```bash
cp .env.example .env
```

**Windows (PowerShell o CMD)**

```bat
copy .env.example .env
```

Editar `.env` con credenciales reales:
- `DB_DRIVER_PATH`
- `DB_SERVER`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `JWT_SECRET_KEY` (mínimo 32 caracteres, generar con `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- `JWT_EXPIRATION_HOURS` (por defecto `8`)
- `API_HOST` (por defecto `127.0.0.1`)
- `API_PORT` (por defecto `8090`)

## Repositorios incluidos

- `donantes_repository.py`: registro, consulta, actualización e inactivación de donantes
- `productos_repository.py`: CRUD de productos
- `donaciones_repository.py`: creación de donaciones y detalle de lotes
- `entregas_repository.py`: creación de entregas y descuentos de inventario
- `inventario_repository.py`: consultas de inventario vigente, lotes por vencer y trazabilidad
- `catalogos_repository.py`: consultas de roles, usuarios, sedes, categorías, lotes y movimientos

## Uso

La API expone endpoints REST protegidos con JWT. Todos los requests (excepto `/health` y `/login`) requieren el header `Authorization: Bearer <token>`.

### Ejemplo mínimo de conexión

**macOS/Linux**

```bash
python3
```

**Windows**

```powershell
py -3
```

```python
from donantes_repository import DonantesRepository

repo = DonantesRepository()
print(repo.get_all())
```

### 7. Configurar contraseña del administrador

```bash
python3 setup_admin.py
```

Este script solicita una contraseña para `admin@trazabilidad.local`, genera el hash bcrypt y lo guarda en la base de datos. Ejecutar **una sola vez** después de cargar el SQL.

### 8. Iniciar la API

**macOS/Linux**

```bash
python3 api_trazabilidad.py
```

**Windows**

```powershell
py -3 api_trazabilidad.py
```

La API quedará disponible en `http://127.0.0.1:8090/trazabilidad/`.

### Consultar ejemplos de uso

Ver [EJEMPLOS.md](EJEMPLOS.md) para ejemplos de autenticación y uso de endpoints via curl.

## Endpoints principales

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/trazabilidad/health` | No | Estado de la API y BD |
| POST | `/trazabilidad/login` | No | Obtener token JWT |
| GET | `/trazabilidad/donantes` | JWT | Listar donantes |
| POST | `/trazabilidad/donantes` | JWT | Crear donante |
| GET | `/trazabilidad/productos` | JWT | Listar productos |
| POST | `/trazabilidad/donaciones` | JWT | Registrar donación |
| GET | `/trazabilidad/inventario/vigente` | JWT | Inventario disponible |
| GET | `/trazabilidad/trazabilidad/lote/{id}` | JWT | Trazabilidad de lote |

## Notas de diseño

- Las escrituras críticas del dominio usan procedimientos almacenados para concentrar reglas de negocio en base de datos.
- Las consultas simples de lectura se resuelven directamente en los repositorios con `SELECT` parametrizados o consultas de catálogo.
- El módulo de donantes implementa borrado lógico con el campo `activo` para no perder referencias históricas en donaciones.

## Contribuir

Las contribuciones son bienvenidas bajo los principios de software libre.

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para directrices.

## Licencia

Este proyecto está licenciado bajo **LGPL 2.1 o posterior**.  
Eres libre de usar, modificar y distribuir este software respetando los términos de la licencia.

Ver [LICENSE](LICENSE) para más detalles.

---

**Nota**: Esta carpeta corresponde a la entrega parcial enfocada en persistencia y base de datos.
