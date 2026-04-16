import datetime


class Donante:

    def __init__(
        self,
        id=0,
        nombre="",
        tipo_documento="CC",
        numero_documento="",
        telefono="",
        email="",
        activo=1,
        fecha=None
    ):
        self.id = id
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.telefono = telefono
        self.email = email
        self.activo = activo
        self.fecha = fecha or datetime.datetime.now()


class Producto:

    def __init__(
        self,
        id=0,
        nombre="",
        categoria_id=1,
        unidad_medida="UN",
        perecedero=1,
        fecha=None
    ):
        self.id = id
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.unidad_medida = unidad_medida
        self.perecedero = perecedero
        self.fecha = fecha or datetime.datetime.now()


class Donacion:

    def __init__(
        self,
        id=0,
        donante_id=0,
        sede_id=1,
        usuario_id=1,
        observacion="",
        fecha=None
    ):
        self.id = id
        self.donante_id = donante_id
        self.sede_id = sede_id
        self.usuario_id = usuario_id
        self.observacion = observacion
        self.fecha = fecha or datetime.datetime.now()


class DetalleDonacion:

    def __init__(
        self,
        donacion_id=0,
        producto_id=0,
        lote_codigo="",
        fecha_vencimiento=None,
        cantidad=0,
        peso_kg=0,
        fecha=None
    ):
        self.donacion_id = donacion_id
        self.producto_id = producto_id
        self.lote_codigo = lote_codigo
        self.fecha_vencimiento = fecha_vencimiento
        self.cantidad = cantidad
        self.peso_kg = peso_kg
        self.fecha = fecha or datetime.datetime.now()


class Entrega:

    def __init__(
        self,
        id=0,
        sede_id=1,
        beneficiario="",
        usuario_id=1,
        observacion="",
        fecha=None
    ):
        self.id = id
        self.sede_id = sede_id
        self.beneficiario = beneficiario
        self.usuario_id = usuario_id
        self.observacion = observacion
        self.fecha = fecha or datetime.datetime.now()


class DetalleEntrega:

    def __init__(self, entrega_id=0, lote_id=0, cantidad=0, peso_kg=0, fecha=None):
        self.entrega_id = entrega_id
        self.lote_id = lote_id
        self.cantidad = cantidad
        self.peso_kg = peso_kg
        self.fecha = fecha or datetime.datetime.now()
