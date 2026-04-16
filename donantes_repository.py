from database_trazabilidad import DatabaseTrazabilidad


class DonantesRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def insert(self, donante):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_donante(?, ?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            donante.nombre,
            donante.tipo_documento,
            donante.numero_documento,
            donante.telefono,
            donante.email,
            donante.fecha
        )

        row = cursor.fetchone()
        donante_id = row.id if row else None

        connection.commit()
        cursor.close()
        connection.close()

        return donante_id

    def update(self, donante):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_update_donante(?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            donante.id,
            donante.nombre,
            donante.telefono,
            donante.email,
            donante.activo
        )

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "SELECT id, nombre, tipo_documento, numero_documento, telefono, email, activo FROM donantes ORDER BY id DESC"
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "tipo_documento": row.tipo_documento,
                "numero_documento": row.numero_documento,
                "telefono": row.telefono,
                "email": row.email,
                "activo": bool(row.activo)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_by_id(self, donante_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT id, nombre, tipo_documento, numero_documento, telefono, email, activo "
            "FROM donantes WHERE id = ?"
        )
        cursor.execute(sql, donante_id)

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if not row:
            return None

        return {
            "id": row.id,
            "nombre": row.nombre,
            "tipo_documento": row.tipo_documento,
            "numero_documento": row.numero_documento,
            "telefono": row.telefono,
            "email": row.email,
            "activo": bool(row.activo)
        }

    def delete(self, donante_id):
        # Soft delete to preserve historical foreign key relationships.
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "UPDATE donantes SET activo = 0 WHERE id = ?"
        cursor.execute(sql, donante_id)

        rows_affected = cursor.rowcount

        connection.commit()
        cursor.close()
        connection.close()

        return rows_affected > 0
