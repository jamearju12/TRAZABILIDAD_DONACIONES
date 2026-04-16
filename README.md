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

## Especificaciones técnicas

- **Lenguaje**: Python 3.8+
- **Base de datos**: MySQL 5.7+ / MariaDB 10.3+
- **Acceso a datos**: pyodbc + patrón Repository + Stored Procedures
- **Gestión de secretos**: Variables de entorno con python-dotenv
- **Licencia**: LGPL 2.1 o posterior

## Alcance de esta entrega

Esta carpeta no incluye la API ni la capa final de servicios. El alcance entregado llega hasta:

- Conexión a base de datos
- Definición de modelos
- Implementación de repositorios
- Script de creación de esquema, datos base y procedimientos almacenados

## Estructura

```
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

## Repositorios incluidos

- `donantes_repository.py`: registro, consulta, actualización e inactivación de donantes
- `productos_repository.py`: CRUD de productos
- `donaciones_repository.py`: creación de donaciones y detalle de lotes
- `entregas_repository.py`: creación de entregas y descuentos de inventario
- `inventario_repository.py`: consultas de inventario vigente, lotes por vencer y trazabilidad
- `catalogos_repository.py`: consultas de roles, usuarios, sedes, categorías, lotes y movimientos

## Uso

Los repositorios se consumen desde scripts Python o pruebas de integración. No hay endpoints HTTP en esta entrega.

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

### Consultar ejemplos de uso

Ver [EJEMPLOS.md](EJEMPLOS.md) para ejemplos de uso directo desde Python.

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
