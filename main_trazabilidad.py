import datetime

from models_trazabilidad import Donante, Producto, Donacion, DetalleDonacion, Entrega, DetalleEntrega
from donantes_repository import DonantesRepository
from productos_repository import ProductosRepository
from donaciones_repository import DonacionesRepository
from entregas_repository import EntregasRepository
from inventario_repository import InventarioRepository


donantes_repo = DonantesRepository()
productos_repo = ProductosRepository()
donaciones_repo = DonacionesRepository()
entregas_repo = EntregasRepository()
inventario_repo = InventarioRepository()

print("\n===== REGISTRANDO DONANTE =====\n")
donante = Donante(
    nombre="Fundacion Manos Unidas",
    tipo_documento="NIT",
    numero_documento="900123456",
    telefono="3001234567",
    email="contacto@manosunidas.org"
)

donante_id = donantes_repo.insert(donante)
print(f"Donante registrado con ID: {donante_id}")

print("\n===== REGISTRANDO PRODUCTO =====\n")
producto = Producto(
    nombre="Arroz integral 1kg",
    categoria_id=1,
    unidad_medida="UN",
    perecedero=0
)

producto_id = productos_repo.insert(producto)
print(f"Producto registrado con ID: {producto_id}")

print("\n===== REGISTRANDO DONACION =====\n")
donacion = Donacion(
    donante_id=donante_id,
    sede_id=1,
    usuario_id=1,
    observacion="Primera donacion de prueba"
)

donacion_id = donaciones_repo.insert(donacion)
print(f"Donacion registrada con ID: {donacion_id}")

lote_codigo = f"L-{donacion_id}-{int(datetime.datetime.now().timestamp())}"

detalle_donacion = DetalleDonacion(
    donacion_id=donacion_id,
    producto_id=producto_id,
    lote_codigo=lote_codigo,
    fecha_vencimiento=(datetime.date.today() + datetime.timedelta(days=180)).isoformat(),
    cantidad=100,
    peso_kg=100
)

lote_id = donaciones_repo.add_detalle(detalle_donacion)
print(f"Lote creado con ID: {lote_id}")

print("\n===== REGISTRANDO ENTREGA =====\n")
entrega = Entrega(
    sede_id=1,
    beneficiario="Comedor comunitario San Jose",
    usuario_id=1,
    observacion="Entrega semanal"
)

entrega_id = entregas_repo.insert(entrega)
print(f"Entrega registrada con ID: {entrega_id}")

detalle_entrega = DetalleEntrega(
    entrega_id=entrega_id,
    lote_id=lote_id,
    cantidad=25,
    peso_kg=25
)

entregas_repo.add_detalle(detalle_entrega)
print("Detalle de entrega registrado")

print("\n===== INVENTARIO VIGENTE =====\n")
inventario = inventario_repo.get_vigente()

for item in inventario:
    print(item)

print("\n===== TRAZABILIDAD DEL LOTE =====\n")
trazabilidad = inventario_repo.get_trazabilidad_lote(lote_id)

for item in trazabilidad:
    print(item)
