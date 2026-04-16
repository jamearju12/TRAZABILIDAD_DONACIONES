from database_trazabilidad import DatabaseTrazabilidad


class InventarioRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def get_vigente(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("CALL sp_get_inventario_vigente()")

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "lote_id": row.lote_id,
                "lote": row.lote,
                "producto": row.producto,
                "categoria": row.categoria,
                "cantidad_actual": float(row.cantidad_actual),
                "peso_kg_actual": float(row.peso_kg_actual),
                "fecha_vencimiento": str(row.fecha_vencimiento) if row.fecha_vencimiento else None
            })

        cursor.close()
        connection.close()

        return resultados

    def get_por_vencer(self, dias=15):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("CALL sp_get_lotes_por_vencer(?)", dias)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "lote_id": row.lote_id,
                "lote": row.lote,
                "producto": row.producto,
                "fecha_vencimiento": str(row.fecha_vencimiento),
                "cantidad_actual": float(row.cantidad_actual),
                "dias_restantes": row.dias_restantes
            })

        cursor.close()
        connection.close()

        return resultados

    def get_trazabilidad_lote(self, lote_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("CALL sp_get_trazabilidad_lote(?)", lote_id)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "lote_id": row.lote_id,
                "lote": row.lote,
                "producto": row.producto,
                "donacion_id": row.donacion_id,
                "donante": row.donante,
                "entrega_id": row.entrega_id,
                "beneficiario": row.beneficiario,
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
