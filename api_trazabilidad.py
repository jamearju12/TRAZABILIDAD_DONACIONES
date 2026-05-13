import datetime
import os
import flask
from dotenv import load_dotenv

from auth_trazabilidad import create_token, requiere_jwt, verificar_credenciales
from database_trazabilidad import DatabaseTrazabilidad
from models_trazabilidad import Donante, Producto, Donacion, DetalleDonacion, Entrega, DetalleEntrega
from donantes_repository import DonantesRepository
from productos_repository import ProductosRepository
from donaciones_repository import DonacionesRepository
from entregas_repository import EntregasRepository
from inventario_repository import InventarioRepository
from catalogos_repository import CatalogosRepository


load_dotenv()

app = flask.Flask(__name__)

donantes_repo = DonantesRepository()
productos_repo = ProductosRepository()
donaciones_repo = DonacionesRepository()
entregas_repo = EntregasRepository()
inventario_repo = InventarioRepository()
catalogos_repo = CatalogosRepository()


def respuesta_ok(datos=None, mensaje="OK"):
    return flask.jsonify({
        "estado": "OK",
        "mensaje": mensaje,
        "fecha": str(datetime.datetime.now()),
        "datos": datos
    })


def respuesta_error(error, status=500):
    return flask.jsonify({
        "estado": "ERROR",
        "mensaje": str(error),
        "fecha": str(datetime.datetime.now())
    }), status


@app.route("/trazabilidad/health", methods=["GET"])
def health():
    try:
        connection = DatabaseTrazabilidad().get_connection()
        connection.close()

        return respuesta_ok({"conexion": "activa"}, "Conexion a base de datos exitosa")

    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/login", methods=["POST"])
def login():
    try:
        data = flask.request.get_json() or {}
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return respuesta_error("Email y password son requeridos", 400)

        usuario = verificar_credenciales(email, password)
        if not usuario:
            return respuesta_error("Credenciales invalidas", 401)

        token = create_token(
            usuario_id=usuario["id"],
            email=usuario["email"],
            rol=usuario["rol"]
        )
        return respuesta_ok({"access_token": token, "token_type": "Bearer"}, "Login exitoso")

    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donantes", methods=["GET"])
@requiere_jwt
def obtener_donantes():
    try:
        return respuesta_ok(donantes_repo.get_all())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donantes", methods=["POST"])
@requiere_jwt
def crear_donante():
    try:
        data = flask.request.get_json() or {}

        donante = Donante(
            nombre=data.get("nombre", ""),
            tipo_documento=data.get("tipo_documento", "CC"),
            numero_documento=data.get("numero_documento", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", "")
        )

        donante_id = donantes_repo.insert(donante)
        return respuesta_ok({"id": donante_id}, "Donante creado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donantes/<int:donante_id>", methods=["GET"])
@requiere_jwt
def obtener_donante_por_id(donante_id):
    try:
        donante = donantes_repo.get_by_id(donante_id)
        if not donante:
            return respuesta_error("Donante no encontrado", 404)
        return respuesta_ok(donante)
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donantes/<int:donante_id>", methods=["PUT"])
@requiere_jwt
def actualizar_donante(donante_id):
    try:
        data = flask.request.get_json() or {}

        donante = Donante(
            id=donante_id,
            nombre=data.get("nombre", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", ""),
            activo=data.get("activo", 1)
        )

        donantes_repo.update(donante)
        return respuesta_ok({"id": donante_id}, "Donante actualizado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donantes/<int:donante_id>", methods=["DELETE"])
@requiere_jwt
def eliminar_donante(donante_id):
    try:
        eliminado = donantes_repo.delete(donante_id)
        if not eliminado:
            return respuesta_error("Donante no encontrado", 404)
        return respuesta_ok({"id": donante_id}, "Donante inactivado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/productos", methods=["GET"])
@requiere_jwt
def obtener_productos():
    try:
        return respuesta_ok(productos_repo.get_all())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/productos", methods=["POST"])
@requiere_jwt
def crear_producto():
    try:
        data = flask.request.get_json() or {}

        producto = Producto(
            nombre=data.get("nombre", ""),
            categoria_id=data.get("categoria_id", 1),
            unidad_medida=data.get("unidad_medida", "UN"),
            perecedero=data.get("perecedero", 1)
        )

        producto_id = productos_repo.insert(producto)
        return respuesta_ok({"id": producto_id}, "Producto creado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/productos/<int:producto_id>", methods=["GET"])
@requiere_jwt
def obtener_producto_por_id(producto_id):
    try:
        producto = productos_repo.get_by_id(producto_id)
        if not producto:
            return respuesta_error("Producto no encontrado", 404)
        return respuesta_ok(producto)
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/productos/<int:producto_id>", methods=["PUT"])
@requiere_jwt
def actualizar_producto(producto_id):
    try:
        data = flask.request.get_json() or {}

        producto = Producto(
            id=producto_id,
            nombre=data.get("nombre", ""),
            categoria_id=data.get("categoria_id", 1),
            unidad_medida=data.get("unidad_medida", "UN"),
            perecedero=data.get("perecedero", 1)
        )

        actualizado = productos_repo.update(producto)
        if not actualizado:
            return respuesta_error("Producto no encontrado", 404)
        return respuesta_ok({"id": producto_id}, "Producto actualizado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/productos/<int:producto_id>", methods=["DELETE"])
@requiere_jwt
def eliminar_producto(producto_id):
    try:
        eliminado = productos_repo.delete(producto_id)
        if not eliminado:
            return respuesta_error("Producto no encontrado o en uso", 404)
        return respuesta_ok({"id": producto_id}, "Producto eliminado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donaciones", methods=["GET"])
@requiere_jwt
def obtener_donaciones():
    try:
        return respuesta_ok(donaciones_repo.get_all())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donaciones/detalles", methods=["GET"])
@requiere_jwt
def obtener_detalles_donacion():
    try:
        return respuesta_ok(donaciones_repo.get_detalles())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donaciones", methods=["POST"])
@requiere_jwt
def crear_donacion():
    try:
        data = flask.request.get_json() or {}

        donacion = Donacion(
            donante_id=data.get("donante_id", 0),
            sede_id=data.get("sede_id", 1),
            usuario_id=data.get("usuario_id", 1),
            observacion=data.get("observacion", "")
        )

        donacion_id = donaciones_repo.insert(donacion)
        return respuesta_ok({"id": donacion_id}, "Donacion creada")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/donaciones/detalles", methods=["POST"])
@requiere_jwt
def agregar_detalle_donacion():
    try:
        data = flask.request.get_json() or {}

        detalle = DetalleDonacion(
            donacion_id=data.get("donacion_id", 0),
            producto_id=data.get("producto_id", 0),
            lote_codigo=data.get("lote_codigo", ""),
            fecha_vencimiento=data.get("fecha_vencimiento"),
            cantidad=data.get("cantidad", 0),
            peso_kg=data.get("peso_kg", 0)
        )

        lote_id = donaciones_repo.add_detalle(detalle)
        return respuesta_ok({"lote_id": lote_id}, "Detalle de donacion registrado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/entregas", methods=["POST"])
@requiere_jwt
def crear_entrega():
    try:
        data = flask.request.get_json() or {}

        entrega = Entrega(
            sede_id=data.get("sede_id", 1),
            beneficiario=data.get("beneficiario", ""),
            usuario_id=data.get("usuario_id", 1),
            observacion=data.get("observacion", "")
        )

        entrega_id = entregas_repo.insert(entrega)
        return respuesta_ok({"id": entrega_id}, "Entrega creada")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/entregas", methods=["GET"])
@requiere_jwt
def obtener_entregas():
    try:
        return respuesta_ok(entregas_repo.get_all())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/entregas/detalles", methods=["POST"])
@requiere_jwt
def agregar_detalle_entrega():
    try:
        data = flask.request.get_json() or {}

        detalle = DetalleEntrega(
            entrega_id=data.get("entrega_id", 0),
            lote_id=data.get("lote_id", 0),
            cantidad=data.get("cantidad", 0),
            peso_kg=data.get("peso_kg", 0)
        )

        entregas_repo.add_detalle(detalle)
        return respuesta_ok(None, "Detalle de entrega registrado")
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/entregas/detalles", methods=["GET"])
@requiere_jwt
def obtener_detalles_entrega():
    try:
        return respuesta_ok(entregas_repo.get_detalles())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/roles", methods=["GET"])
@requiere_jwt
def obtener_roles():
    try:
        return respuesta_ok(catalogos_repo.get_roles())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/usuarios", methods=["GET"])
@requiere_jwt
def obtener_usuarios():
    try:
        return respuesta_ok(catalogos_repo.get_usuarios())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/sedes", methods=["GET"])
@requiere_jwt
def obtener_sedes():
    try:
        return respuesta_ok(catalogos_repo.get_sedes())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/categorias", methods=["GET"])
@requiere_jwt
def obtener_categorias():
    try:
        return respuesta_ok(catalogos_repo.get_categorias())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/lotes", methods=["GET"])
@requiere_jwt
def obtener_lotes():
    try:
        return respuesta_ok(catalogos_repo.get_lotes())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/movimientos", methods=["GET"])
@requiere_jwt
def obtener_movimientos():
    try:
        return respuesta_ok(catalogos_repo.get_movimientos())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/inventario", methods=["GET"])
@requiere_jwt
def obtener_inventario_vigente():
    try:
        return respuesta_ok(inventario_repo.get_vigente())
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/inventario/por-vencer", methods=["GET"])
@requiere_jwt
def obtener_lotes_por_vencer():
    try:
        dias = int(flask.request.args.get("dias", 15))
        return respuesta_ok(inventario_repo.get_por_vencer(dias))
    except Exception as e:
        return respuesta_error(e)


@app.route("/trazabilidad/lotes/<int:lote_id>/trazabilidad", methods=["GET"])
@requiere_jwt
def obtener_trazabilidad_lote(lote_id):
    try:
        return respuesta_ok(inventario_repo.get_trazabilidad_lote(lote_id))
    except Exception as e:
        return respuesta_error(e)


if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8090"))
    app.run(host=host, port=port)
