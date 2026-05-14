# Ejemplos de uso - API REST y repositorios

## Preparación previa

```bash
# 1. Crear archivo .env desde .env.example
cp .env.example .env

# 2. Editar .env con credenciales reales
nano .env

# 3. Instalar dependencias
python3 -m pip install -r requirements.txt

# 4. Cargar el esquema SQL
mysql -u root -p < trazabilidad_alimentos.sql

# 5. Configurar contraseña del administrador
python3 setup_admin.py

# 6. Iniciar la API
python3 api_trazabilidad.py
```

## Autenticación

### Obtener token JWT

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@trazabilidad.local", "password": "tu-contraseña"}'
```

Guardar el token para usarlo en los siguientes ejemplos:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8090/trazabilidad/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@trazabilidad.local", "password": "tu-contraseña"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['datos']['access_token'])")
```

## Ejemplos via API REST (curl)

### Verificar estado

```bash
curl -s http://127.0.0.1:8090/trazabilidad/health | python3 -m json.tool
```

### Listar donantes

```bash
curl -s http://127.0.0.1:8090/trazabilidad/donantes \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Crear un donante

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donantes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Asociacion Red Solidaria",
    "tipo_documento": "NIT",
    "numero_documento": "901555777-1",
    "telefono": "3100000000",
    "email": "contacto@redsolidaria.org"
  }'
```

### Listar productos

```bash
curl -s http://127.0.0.1:8090/trazabilidad/productos \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Registrar una donación

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donaciones \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "donante_id": 1,
    "sede_id": 1,
    "usuario_id": 1,
    "observacion": "Donacion para inventario base"
  }'
```

### Agregar lote a una donación

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donaciones/1/detalle \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "producto_id": 1,
    "lote_codigo": "L-2026-001",
    "fecha_vencimiento": "2026-12-15",
    "cantidad": 120,
    "peso_kg": 120
  }'
```

### Consultar inventario vigente

```bash
curl -s http://127.0.0.1:8090/trazabilidad/inventario/vigente \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Consultar trazabilidad de un lote

```bash
curl -s http://127.0.0.1:8090/trazabilidad/trazabilidad/lote/1 \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Uso desde Python

### Consultar donantes

```python
from donantes_repository import DonantesRepository

repo = DonantesRepository()
donantes = repo.get_all()

for donante in donantes:
    print(donante)
```

### Crear un donante

```python
from donantes_repository import DonantesRepository
from models_trazabilidad import Donante

repo = DonantesRepository()

nuevo = Donante(
    nombre="Asociacion Red Solidaria",
    tipo_documento="NIT",
    numero_documento="901555777-1",
    telefono="3100000000",
    email="contacto@redsolidaria.org"
)

donante_id = repo.insert(nuevo)
print(donante_id)
```

### Actualizar e inactivar donantes

```python
from donantes_repository import DonantesRepository
from models_trazabilidad import Donante

repo = DonantesRepository()

repo.update(Donante(
    id=1,
    nombre="Asociacion Red Solidaria Actualizada",
    telefono="3111111111",
    email="nuevo@redsolidaria.org",
    activo=1
))

repo.delete(1)
```

### Crear un producto

```python
from productos_repository import ProductosRepository
from models_trazabilidad import Producto

repo = ProductosRepository()

producto_id = repo.insert(Producto(
    nombre="Frijol cargamanto",
    categoria_id=1,
    unidad_medida="KG",
    perecedero=0
))

print(producto_id)
```

### Registrar una donación y su lote

```python
from donaciones_repository import DonacionesRepository
from models_trazabilidad import Donacion, DetalleDonacion

repo = DonacionesRepository()

donacion_id = repo.insert(Donacion(
    donante_id=1,
    sede_id=1,
    usuario_id=1,
    observacion="Donacion para inventario base"
))

lote_id = repo.add_detalle(DetalleDonacion(
    donacion_id=donacion_id,
    producto_id=1,
    lote_codigo="L-2026-001",
    fecha_vencimiento="2026-12-15",
    cantidad=120,
    peso_kg=120
))

print(donacion_id, lote_id)
```

### Registrar una entrega

```python
from entregas_repository import EntregasRepository
from models_trazabilidad import Entrega, DetalleEntrega

repo = EntregasRepository()

entrega_id = repo.insert(Entrega(
    sede_id=1,
    beneficiario="Comedor Esperanza",
    usuario_id=1,
    observacion="Entrega programada"
))

repo.add_detalle(DetalleEntrega(
    entrega_id=entrega_id,
    lote_id=1,
    cantidad=20,
    peso_kg=20
))
```

### Consultar inventario y trazabilidad

```python
from inventario_repository import InventarioRepository

repo = InventarioRepository()

print(repo.get_vigente())
print(repo.get_por_vencer(30))
print(repo.get_trazabilidad_lote(1))
```

## Nota de diseño

El método `delete` de `DonantesRepository` implementa borrado lógico: actualiza el campo `activo` a `0` en lugar de eliminar físicamente el registro. Esto conserva la integridad histórica de las donaciones relacionadas.
