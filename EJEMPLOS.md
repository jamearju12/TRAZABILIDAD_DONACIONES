# Ejemplos de uso - API Endpoints

## Setup previo

```bash
# 1. Crear archivo .env desde .env.example
cp .env.example .env

# 2. Editar .env con credenciales reales (incluir JWT_SECRET_KEY)
nano .env

# 3. Instalar dependencias
python3 -m pip install -r requirements.txt

# 4. Cargar el esquema SQL
mysql -u root -p < trazabilidad_alimentos.sql

# 5. Configurar contraseña del admin (solo la primera vez)
python3 setup_admin.py

# 6. Levantar la API
python3 api_trazabilidad.py
```

## Autenticación

Todos los endpoints (excepto `/health` y `/login`) requieren un token JWT en el header `Authorization`.

### Obtener Token (Login)

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@trazabilidad.local", "password": "tu-contraseña"}' | jq .
```

Guarda el `access_token` de la respuesta. En los ejemplos siguientes se asume que lo tienes guardado:

```bash
TOKEN="pega-aqui-el-access_token"
```

O expórtalo automáticamente:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8090/trazabilidad/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@trazabilidad.local", "password": "tu-contraseña"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['datos']['access_token'])")
```

### Health Check (no requiere token)

```bash
curl -s http://127.0.0.1:8090/trazabilidad/health | jq .
```

## Ejemplos con curl

### Crear Donante

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donantes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nombre": "Fundacion Comida Para Todos",
    "tipo_documento": "NIT",
    "numero_documento": "900112233",
    "telefono": "3101234567",
    "email": "contacto@comidaparatodos.org"
  }'
```

### Listar Donantes

```bash
curl -s http://127.0.0.1:8090/trazabilidad/donantes \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Crear Producto

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/productos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nombre": "Lentejas 1kg",
    "categoria_id": 1,
    "unidad_medida": "UN",
    "perecedero": 0
  }'
```

### Listar Productos

```bash
curl -s http://127.0.0.1:8090/trazabilidad/productos \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Crear Donacion

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donaciones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "donante_id": 1,
    "sede_id": 1,
    "usuario_id": 1,
    "observacion": "Donacion inicial de prueba"
  }'
```

### Agregar Detalle a Donacion

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/donaciones/detalles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "donacion_id": 1,
    "producto_id": 1,
    "lote_codigo": "LOTE-001-2026",
    "fecha_vencimiento": "2026-10-08",
    "cantidad": 50,
    "peso_kg": 50
  }'
```

### Crear Entrega

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/entregas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "sede_id": 1,
    "beneficiario": "Comedor Comunitario El Buen Vivir",
    "usuario_id": 1,
    "observacion": "Entrega semanal"
  }'
```

### Agregar Detalle a Entrega

```bash
curl -s -X POST http://127.0.0.1:8090/trazabilidad/entregas/detalles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "entrega_id": 1,
    "lote_id": 1,
    "cantidad": 25,
    "peso_kg": 25
  }'
```

### Ver Inventario Vigente

```bash
curl -s http://127.0.0.1:8090/trazabilidad/inventario \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Ver Lotes por Vencer (próximos 30 días)

```bash
curl -s "http://127.0.0.1:8090/trazabilidad/inventario/por-vencer?dias=30" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Obtener Trazabilidad Completa de un Lote

```bash
curl -s http://127.0.0.1:8090/trazabilidad/lotes/1/trazabilidad \
  -H "Authorization: Bearer $TOKEN" | jq .
```

## Flujo completo de prueba

```bash
python3 main_trazabilidad.py
```

Este script ejecuta un flujo CRUD completo: crea donante, producto, donación, entrega y muestra inventario e historial.
