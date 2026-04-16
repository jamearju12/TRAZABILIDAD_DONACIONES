from database_trazabilidad import DatabaseTrazabilidad


class EntregasRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def insert(self, entrega):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_entrega(?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            entrega.sede_id,
            entrega.beneficiario,
            entrega.usuario_id,
            entrega.observacion,
            entrega.fecha
        )

        row = cursor.fetchone()
        entrega_id = row.id if row else None

        connection.commit()
        cursor.close()
        connection.close()

        return entrega_id

    def add_detalle(self, detalle):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_detalle_entrega(?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            detalle.entrega_id,
            detalle.lote_id,
            detalle.cantidad,
            detalle.peso_kg,
            detalle.fecha
        )

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT e.id, s.nombre AS sede, e.beneficiario, u.nombre AS usuario, e.observacion, e.fecha_creacion "
            "FROM entregas e "
            "INNER JOIN sedes s ON s.id = e.sede_id "
            "INNER JOIN usuarios u ON u.id = e.usuario_id "
            "ORDER BY e.id DESC"
        )
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "sede": row.sede,
                "beneficiario": row.beneficiario,
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
            "SELECT de.id, de.entrega_id, de.lote_id, l.codigo AS lote, p.nombre AS producto, "
            "de.cantidad, de.peso_kg, de.fecha_creacion "
            "FROM detalle_entrega de "
            "INNER JOIN lotes l ON l.id = de.lote_id "
            "INNER JOIN productos p ON p.id = l.producto_id "
            "ORDER BY de.id DESC"
        )
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "entrega_id": row.entrega_id,
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
