from database_trazabilidad import DatabaseTrazabilidad


class CatalogosRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def get_roles(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, nombre, fecha_creacion FROM roles ORDER BY id DESC")

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_usuarios(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT u.id, u.nombre, u.email, r.nombre AS rol, u.activo, u.fecha_creacion "
            "FROM usuarios u "
            "INNER JOIN roles r ON r.id = u.rol_id "
            "ORDER BY u.id DESC"
        )
        cursor.execute(sql)

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "email": row.email,
                "rol": row.rol,
                "activo": bool(row.activo),
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_sedes(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, nombre, direccion, ciudad, fecha_creacion FROM sedes ORDER BY id DESC")

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "direccion": row.direccion,
                "ciudad": row.ciudad,
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_categorias(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, nombre, descripcion, fecha_creacion FROM categorias_alimento ORDER BY id DESC")

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "descripcion": row.descripcion,
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_lotes(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT l.id, l.codigo, p.nombre AS producto, l.donacion_id, l.fecha_vencimiento, "
            "l.cantidad_inicial, l.cantidad_actual, l.peso_kg_inicial, l.peso_kg_actual, l.fecha_creacion "
            "FROM lotes l "
            "INNER JOIN productos p ON p.id = l.producto_id "
            "ORDER BY l.id DESC"
        )
        cursor.execute(sql)

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "codigo": row.codigo,
                "producto": row.producto,
                "donacion_id": row.donacion_id,
                "fecha_vencimiento": str(row.fecha_vencimiento) if row.fecha_vencimiento else None,
                "cantidad_inicial": float(row.cantidad_inicial),
                "cantidad_actual": float(row.cantidad_actual),
                "peso_kg_inicial": float(row.peso_kg_inicial),
                "peso_kg_actual": float(row.peso_kg_actual),
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_movimientos(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT m.id, m.lote_id, l.codigo AS lote, m.tipo_movimiento, m.referencia_tipo, "
            "m.referencia_id, m.cantidad, m.peso_kg, m.fecha_creacion "
            "FROM movimientos_inventario m "
            "INNER JOIN lotes l ON l.id = m.lote_id "
            "ORDER BY m.id DESC"
        )
        cursor.execute(sql)

        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "lote_id": row.lote_id,
                "lote": row.lote,
                "tipo_movimiento": row.tipo_movimiento,
                "referencia_tipo": row.referencia_tipo,
                "referencia_id": row.referencia_id,
                "cantidad": float(row.cantidad),
                "peso_kg": float(row.peso_kg),
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados
