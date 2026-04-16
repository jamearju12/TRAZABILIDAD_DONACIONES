from database_trazabilidad import DatabaseTrazabilidad


class ProductosRepository:

    def __init__(self):
        self.db = DatabaseTrazabilidad()

    def insert(self, producto):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "CALL sp_insert_producto(?, ?, ?, ?, ?)"

        cursor.execute(
            sql,
            producto.nombre,
            producto.categoria_id,
            producto.unidad_medida,
            producto.perecedero,
            producto.fecha
        )

        row = cursor.fetchone()
        producto_id = row.id if row else None

        connection.commit()
        cursor.close()
        connection.close()

        return producto_id

    def get_all(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT p.id, p.nombre, c.nombre AS categoria, p.unidad_medida, p.perecedero "
            "FROM productos p INNER JOIN categorias_alimento c ON c.id = p.categoria_id "
            "ORDER BY p.id DESC"
        )
        cursor.execute(sql)

        resultados = []

        for row in cursor.fetchall():
            resultados.append({
                "id": row.id,
                "nombre": row.nombre,
                "categoria": row.categoria,
                "unidad_medida": row.unidad_medida,
                "perecedero": bool(row.perecedero)
            })

        cursor.close()
        connection.close()

        return resultados

    def get_by_id(self, producto_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "SELECT p.id, p.nombre, p.categoria_id, c.nombre AS categoria, p.unidad_medida, p.perecedero "
            "FROM productos p "
            "INNER JOIN categorias_alimento c ON c.id = p.categoria_id "
            "WHERE p.id = ?"
        )
        cursor.execute(sql, producto_id)

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if not row:
            return None

        return {
            "id": row.id,
            "nombre": row.nombre,
            "categoria_id": row.categoria_id,
            "categoria": row.categoria,
            "unidad_medida": row.unidad_medida,
            "perecedero": bool(row.perecedero)
        }

    def update(self, producto):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = (
            "UPDATE productos "
            "SET nombre = ?, categoria_id = ?, unidad_medida = ?, perecedero = ? "
            "WHERE id = ?"
        )

        cursor.execute(
            sql,
            producto.nombre,
            producto.categoria_id,
            producto.unidad_medida,
            producto.perecedero,
            producto.id
        )

        rows_affected = cursor.rowcount

        connection.commit()
        cursor.close()
        connection.close()

        return rows_affected > 0

    def delete(self, producto_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        sql = "DELETE FROM productos WHERE id = ?"
        cursor.execute(sql, producto_id)

        rows_affected = cursor.rowcount

        connection.commit()
        cursor.close()
        connection.close()

        return rows_affected > 0
