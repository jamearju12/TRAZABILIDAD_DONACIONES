# Trazabilidad de Donaciones de Alimentos

[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1.html)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Framework-Flask-brightgreen)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-blue)](https://www.mysql.com/)

Sistema integral de trazabilidad para gestión de donaciones de alimentos en fundaciones y organizaciones sin ánimo de lucro, bajo principios de software libre.

## Características principales

✅ **Autenticación JWT** - Acceso seguro con tokens firmados y expiración configurable  
✅ **Contraseñas encriptadas** - Hash bcrypt con factor de costo 12 (estándar OWASP)  
✅ **Registro de donantes** - Administración centralizada de donadores  
✅ **Gestión de productos** - Catálogo de alimentos por categoría  
✅ **Control de lotes** - Seguimiento de códigos, vencimientos y cantidades  
✅ **Registros de donaciones** - Entrada de alimentos al sistema  
✅ **Entregas a beneficiarios** - Control de distribución de alimentos  
✅ **Inventario vigente** - Consulta de stock disponible  
✅ **Alertas de vencimiento** - Identificación de lotes próximos a vencer  
✅ **Trazabilidad completa** - Historial completo de cada lote desde origen hasta destino  

## Especificaciones técnicas

- **Lenguaje**: Python 3.8+
- **Framework**: Flask 3.0+
- **Base de datos**: MySQL 5.7+ / MariaDB 10.3+
- **ORM/Conexión**: pyodbc + patrón Repository + Stored Procedures
- **Autenticación**: PyJWT 2.8+ (HS256)
- **Encriptación**: bcrypt 4.0+ (cost factor 12)
- **Gestión de secretos**: Variables de entorno con python-dotenv
- **Licencia**: LGPL 2.1 o posterior

## Estructura

\`\`\`
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
\`\`\`

## Instalación rápida

### 1. Requisitos previos

- Python 3.8+
- MySQL 5.7+ o MariaDB 10.3+
- pip (gestor de paquetes Python)

### 2. Clonar o descargar

\`\`\`bash
git clone https://github.com/jamearju12/TRAZABILIDAD_DONACIONES.git
cd TRAZABILIDAD_DONACIONES
\`\`\`

### 3. Crear entorno virtual

**macOS/Linux**

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
\`\`\`

**Windows (PowerShell)**

\`\`\`powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
\`\`\`

**Windows (CMD)**

\`\`\`bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
\`\`\`

### 4. Instalar dependencias

**macOS/Linux**

\`\`\`bash
python3 -m pip install -r requirements.txt
\`\`\`

**Windows**

\`\`\`powershell
py -3 -m pip install -r requirements.txt
\`\`\`

### 5. Configurar base de datos

\`\`\`bash
mysql -u root -p < trazabilidad_alimentos.sql
\`\`\`

### 6. Configurar secretos

**macOS/Linux**

\`\`\`bash
cp .env.example .env
\`\`\`

**Windows (PowerShell o CMD)**

\`\`\`bat
copy .env.example .env
\`\`\`

Editar \`.env\` con credenciales reales:
- \`DB_DRIVER_PATH\`
- \`DB_SERVER\`
- \`DB_NAME\`
- \`DB_USER\`
- \`DB_PASSWORD\`
- \`API_HOST\` (por defecto \`127.0.0.1\`)
- \`API_PORT\` (por defecto \`8090\`)
- \`JWT_SECRET_KEY\` — clave secreta para firmar tokens (mínimo 32 caracteres). Generar con:
  \`\`\`bash
  python3 -c "import secrets; print(secrets.token_hex(32))"
  \`\`\`
- \`JWT_EXPIRATION_HOURS\` — tiempo de vida del token (por defecto \`8\`)

### 7. Configurar contraseña del administrador

**macOS/Linux**

\`\`\`bash
python3 setup_admin.py
\`\`\`

**Windows**

\`\`\`powershell
py -3 setup_admin.py
\`\`\`

Este script solicita la contraseña del usuario \`admin@trazabilidad.local\` y guarda el hash bcrypt en la base de datos. Ejecutar **una sola vez** tras cargar el SQL.

### 8. Iniciar la API

**macOS/Linux**

\`\`\`bash
python3 api_trazabilidad.py
\`\`\`

**Windows**

\`\`\`powershell
py -3 api_trazabilidad.py
\`\`\`

La API estará disponible en: \`http://127.0.0.1:8090\`

### Consultar ejemplos de uso

Ver [EJEMPLOS.md](EJEMPLOS.md) para ejemplos completos con curl.

## Endpoints principales

### Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | \`/trazabilidad/login\` | Obtener token JWT | No requerida |
| GET | \`/trazabilidad/health\` | Verificar estado de la API | No requerida |

> Todos los demás endpoints requieren el header: \`Authorization: Bearer <token>\`

### Donantes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | \`/trazabilidad/donantes\` | Listar donantes |
| POST | \`/trazabilidad/donantes\` | Crear donante |
| GET | \`/trazabilidad/donantes/<int:donante_id>\` | Obtener donante por ID |
| PUT | \`/trazabilidad/donantes/<int:donante_id>\` | Actualizar donante |
| DELETE | \`/trazabilidad/donantes/<int:donante_id>\` | Inactivar donante |

### Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | \`/trazabilidad/productos\` | Listar productos |
| POST | \`/trazabilidad/productos\` | Crear producto |
| GET | \`/trazabilidad/productos/<int:producto_id>\` | Obtener producto por ID |
| PUT | \`/trazabilidad/productos/<int:producto_id>\` | Actualizar producto |
| DELETE | \`/trazabilidad/productos/<int:producto_id>\` | Eliminar producto |

### Donaciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | \`/trazabilidad/donaciones\` | Listar donaciones |
| POST | \`/trazabilidad/donaciones\` | Crear donación |
| GET | \`/trazabilidad/donaciones/detalles\` | Listar detalles de donación |
| POST | \`/trazabilidad/donaciones/detalles\` | Agregar detalle de donación |

### Entregas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | \`/trazabilidad/entregas\` | Listar entregas |
| POST | \`/trazabilidad/entregas\` | Crear entrega |
| GET | \`/trazabilidad/entregas/detalles\` | Listar detalles de entrega |
| POST | \`/trazabilidad/entregas/detalles\` | Agregar detalle de entrega |

### Catálogos y trazabilidad

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | \`/trazabilidad/roles\` | Listar roles |
| GET | \`/trazabilidad/usuarios\` | Listar usuarios |
| GET | \`/trazabilidad/sedes\` | Listar sedes |
| GET | \`/trazabilidad/categorias\` | Listar categorías de alimento |
| GET | \`/trazabilidad/lotes\` | Listar lotes |
| GET | \`/trazabilidad/movimientos\` | Listar movimientos de inventario |
| GET | \`/trazabilidad/inventario\` | Ver inventario vigente |
| GET | \`/trazabilidad/inventario/por-vencer\` | Lotes próximos a vencer |
| GET | \`/trazabilidad/lotes/<int:lote_id>/trazabilidad\` | Historial completo del lote |

## Contribuir

Las contribuciones son bienvenidas bajo los principios de software libre.

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para directrices.

## Licencia

Este proyecto está licenciado bajo **LGPL 2.1 o posterior**.  
Eres libre de usar, modificar y distribuir este software respetando los términos de la licencia.

Ver [LICENSE](LICENSE) para más detalles.

---

**Nota**: Sistema diseñado bajo principios de software libre y transparencia.
