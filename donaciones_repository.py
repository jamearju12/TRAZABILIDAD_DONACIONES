from database_trazabilidad import DatabaseTrazabilidad


class DonacionesRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def insert(self, donacion):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_donacion(?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            donacion.donante_id,
            donacion.sede_id,
            donacion.usuario_id,
            donacion.observacion,
            donacion.fecha
        )

        row = cursor.fetchone()
        donacion_id = row.id if row else None

        connection.commit()
        cursor.close()
        connection.close()

        return donacion_id

    def add_detalle(self, detalle):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_detalle_donacion(?, ?, ?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            detalle.donacion_id,
            detalle.producto_id,
            detalle.lote_codigo,
            detalle.fecha_vencimiento,
            detalle.cantidad,
            detalle.peso_kg,
            detalle.fecha
        )

        row = cursor.fetchone()
        lote_id = row.lote_id if row else None

        connection.commit()
        cursor.close()
        connection.close()

        return lote_id

    def get_all(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT d.id, dn.nombre AS donante, s.nombre AS sede, u.nombre AS usuario, d.observacion, d.fecha_creacion "
            "FROM donaciones d "
            "INNER JOIN donantes dn ON dn.id = d.donante_id "
            "INNER JOIN sedes s ON s.id = d.sede_id "
            "INNER JOIN usuarios u ON u.id = d.usuario_id "
            "ORDER BY d.id DESC"
        )
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "donante": row.donante,
                "sede": row.sede,
                "usuario": row.usuario,
                "observacion": row.observacion,
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_detalles(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT dd.id, dd.donacion_id, l.id AS lote_id, l.codigo AS lote, p.nombre AS producto, "
            "dd.cantidad, dd.peso_kg, dd.fecha_creacion "
            "FROM detalle_donacion dd "
            "INNER JOIN lotes l ON l.id = dd.lote_id "
            "INNER JOIN productos p ON p.id = l.producto_id "
            "ORDER BY dd.id DESC"
        )
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "donacion_id": row.donacion_id,
                "lote_id": row.lote_id,
                "lote": row.lote,
                "producto": row.producto,
                "cantidad": float(row.cantidad),
                "peso_kg": float(row.peso_kg),
                "fecha": str(row.fecha_creacion)
            })

        cursor.close()
        connection.close()

        return resultados
