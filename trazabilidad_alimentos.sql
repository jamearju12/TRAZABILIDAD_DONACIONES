CREATE DATABASE IF NOT EXISTS db_trazabilidad_alimentos;

USE db_trazabilidad_alimentos;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    fecha_creacion DATETIME NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    rol_id INT NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles(id)
);

CREATE TABLE sedes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(250),
    ciudad VARCHAR(100) NOT NULL,
    fecha_creacion DATETIME NOT NULL
);

CREATE TABLE donantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo_documento VARCHAR(20) NOT NULL,
    numero_documento VARCHAR(40) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    email VARCHAR(150),
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL
);

CREATE TABLE categorias_alimento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE,
    descripcion VARCHAR(250),
    fecha_creacion DATETIME NOT NULL
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria_id INT NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,
    perecedero TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (categoria_id)
        REFERENCES categorias_alimento(id)
);

CREATE TABLE donaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donante_id INT NOT NULL,
    sede_id INT NOT NULL,
    usuario_id INT NOT NULL,
    observacion VARCHAR(250),
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_donaciones_donantes
        FOREIGN KEY (donante_id)
        REFERENCES donantes(id),
    CONSTRAINT fk_donaciones_sedes
        FOREIGN KEY (sede_id)
        REFERENCES sedes(id),
    CONSTRAINT fk_donaciones_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);

CREATE TABLE lotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(60) NOT NULL UNIQUE,
    producto_id INT NOT NULL,
    donacion_id INT NOT NULL,
    fecha_vencimiento DATE,
    cantidad_inicial DECIMAL(12,2) NOT NULL,
    cantidad_actual DECIMAL(12,2) NOT NULL,
    peso_kg_inicial DECIMAL(12,2) NOT NULL DEFAULT 0,
    peso_kg_actual DECIMAL(12,2) NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_lotes_productos
        FOREIGN KEY (producto_id)
        REFERENCES productos(id),
    CONSTRAINT fk_lotes_donaciones
        FOREIGN KEY (donacion_id)
        REFERENCES donaciones(id)
);

CREATE TABLE detalle_donacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donacion_id INT NOT NULL,
    lote_id INT NOT NULL,
    cantidad DECIMAL(12,2) NOT NULL,
    peso_kg DECIMAL(12,2) NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_detalle_donacion_donaciones
        FOREIGN KEY (donacion_id)
        REFERENCES donaciones(id),
    CONSTRAINT fk_detalle_donacion_lotes
        FOREIGN KEY (lote_id)
        REFERENCES lotes(id)
);

CREATE TABLE entregas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sede_id INT NOT NULL,
    beneficiario VARCHAR(150) NOT NULL,
    usuario_id INT NOT NULL,
    observacion VARCHAR(250),
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_entregas_sedes
        FOREIGN KEY (sede_id)
        REFERENCES sedes(id),
    CONSTRAINT fk_entregas_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);

CREATE TABLE detalle_entrega (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entrega_id INT NOT NULL,
    lote_id INT NOT NULL,
    cantidad DECIMAL(12,2) NOT NULL,
    peso_kg DECIMAL(12,2) NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_detalle_entrega_entregas
        FOREIGN KEY (entrega_id)
        REFERENCES entregas(id),
    CONSTRAINT fk_detalle_entrega_lotes
        FOREIGN KEY (lote_id)
        REFERENCES lotes(id)
);

CREATE TABLE movimientos_inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lote_id INT NOT NULL,
    tipo_movimiento VARCHAR(20) NOT NULL,
    referencia_tipo VARCHAR(20) NOT NULL,
    referencia_id INT NOT NULL,
    cantidad DECIMAL(12,2) NOT NULL,
    peso_kg DECIMAL(12,2) NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL,
    CONSTRAINT fk_movimientos_lotes
        FOREIGN KEY (lote_id)
        REFERENCES lotes(id)
);

INSERT INTO roles (nombre, fecha_creacion)
SELECT 'ADMIN', NOW()
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE nombre = 'ADMIN');

INSERT INTO sedes (nombre, direccion, ciudad, fecha_creacion)
SELECT 'Sede Central', 'Calle 1 # 10-20', 'Bogota', NOW()
WHERE NOT EXISTS (SELECT 1 FROM sedes WHERE nombre = 'Sede Central');

INSERT INTO usuarios (nombre, email, rol_id, activo, fecha_creacion)
SELECT 'Usuario Admin', 'admin@trazabilidad.local', r.id, 1, NOW()
FROM roles r
WHERE r.nombre = 'ADMIN'
  AND NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'admin@trazabilidad.local');

INSERT INTO categorias_alimento (nombre, descripcion, fecha_creacion)
SELECT 'No perecederos', 'Productos secos y enlatados', NOW()
WHERE NOT EXISTS (SELECT 1 FROM categorias_alimento WHERE nombre = 'No perecederos');

DELIMITER $$

CREATE PROCEDURE sp_insert_donante(
    IN p_nombre VARCHAR(150),
    IN p_tipo_documento VARCHAR(20),
    IN p_numero_documento VARCHAR(40),
    IN p_telefono VARCHAR(30),
    IN p_email VARCHAR(150),
    IN p_fecha DATETIME
)
BEGIN
    INSERT INTO donantes(
        nombre,
        tipo_documento,
        numero_documento,
        telefono,
        email,
        activo,
        fecha_creacion
    )
    VALUES(
        p_nombre,
        p_tipo_documento,
        p_numero_documento,
        p_telefono,
        p_email,
        1,
        p_fecha
    );

    SELECT LAST_INSERT_ID() AS id;
END$$

CREATE PROCEDURE sp_update_donante(
    IN p_id INT,
    IN p_nombre VARCHAR(150),
    IN p_telefono VARCHAR(30),
    IN p_email VARCHAR(150),
    IN p_activo TINYINT
)
BEGIN
    UPDATE donantes
    SET nombre = p_nombre,
        telefono = p_telefono,
        email = p_email,
        activo = p_activo
    WHERE id = p_id;
END$$

CREATE PROCEDURE sp_insert_producto(
    IN p_nombre VARCHAR(150),
    IN p_categoria_id INT,
    IN p_unidad_medida VARCHAR(20),
    IN p_perecedero TINYINT,
    IN p_fecha DATETIME
)
BEGIN
    INSERT INTO productos(
        nombre,
        categoria_id,
        unidad_medida,
        perecedero,
        fecha_creacion
    )
    VALUES(
        p_nombre,
        p_categoria_id,
        p_unidad_medida,
        p_perecedero,
        p_fecha
    );

    SELECT LAST_INSERT_ID() AS id;
END$$

CREATE PROCEDURE sp_insert_donacion(
    IN p_donante_id INT,
    IN p_sede_id INT,
    IN p_usuario_id INT,
    IN p_observacion VARCHAR(250),
    IN p_fecha DATETIME
)
BEGIN
    INSERT INTO donaciones(
        donante_id,
        sede_id,
        usuario_id,
        observacion,
        fecha_creacion
    )
    VALUES(
        p_donante_id,
        p_sede_id,
        p_usuario_id,
        p_observacion,
        p_fecha
    );

    SELECT LAST_INSERT_ID() AS id;
END$$

CREATE PROCEDURE sp_insert_detalle_donacion(
    IN p_donacion_id INT,
    IN p_producto_id INT,
    IN p_lote_codigo VARCHAR(60),
    IN p_fecha_vencimiento DATE,
    IN p_cantidad DECIMAL(12,2),
    IN p_peso_kg DECIMAL(12,2),
    IN p_fecha DATETIME
)
BEGIN
    DECLARE v_lote_id INT;

    INSERT INTO lotes(
        codigo,
        producto_id,
        donacion_id,
        fecha_vencimiento,
        cantidad_inicial,
        cantidad_actual,
        peso_kg_inicial,
        peso_kg_actual,
        fecha_creacion
    )
    VALUES(
        p_lote_codigo,
        p_producto_id,
        p_donacion_id,
        p_fecha_vencimiento,
        p_cantidad,
        p_cantidad,
        p_peso_kg,
        p_peso_kg,
        p_fecha
    );

    SET v_lote_id = LAST_INSERT_ID();

    INSERT INTO detalle_donacion(
        donacion_id,
        lote_id,
        cantidad,
        peso_kg,
        fecha_creacion
    )
    VALUES(
        p_donacion_id,
        v_lote_id,
        p_cantidad,
        p_peso_kg,
        p_fecha
    );

    INSERT INTO movimientos_inventario(
        lote_id,
        tipo_movimiento,
        referencia_tipo,
        referencia_id,
        cantidad,
        peso_kg,
        fecha_creacion
    )
    VALUES(
        v_lote_id,
        'ENTRADA',
        'DONACION',
        p_donacion_id,
        p_cantidad,
        p_peso_kg,
        p_fecha
    );

    SELECT v_lote_id AS lote_id;
END$$

CREATE PROCEDURE sp_insert_entrega(
    IN p_sede_id INT,
    IN p_beneficiario VARCHAR(150),
    IN p_usuario_id INT,
    IN p_observacion VARCHAR(250),
    IN p_fecha DATETIME
)
BEGIN
    INSERT INTO entregas(
        sede_id,
        beneficiario,
        usuario_id,
        observacion,
        fecha_creacion
    )
    VALUES(
        p_sede_id,
        p_beneficiario,
        p_usuario_id,
        p_observacion,
        p_fecha
    );

    SELECT LAST_INSERT_ID() AS id;
END$$

CREATE PROCEDURE sp_insert_detalle_entrega(
    IN p_entrega_id INT,
    IN p_lote_id INT,
    IN p_cantidad DECIMAL(12,2),
    IN p_peso_kg DECIMAL(12,2),
    IN p_fecha DATETIME
)
BEGIN
    DECLARE v_cantidad_actual DECIMAL(12,2);
    DECLARE v_peso_actual DECIMAL(12,2);

    SELECT cantidad_actual, peso_kg_actual
    INTO v_cantidad_actual, v_peso_actual
    FROM lotes
    WHERE id = p_lote_id
    FOR UPDATE;

    IF v_cantidad_actual IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Lote no encontrado';
    END IF;

    IF v_cantidad_actual < p_cantidad THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock insuficiente para la entrega';
    END IF;

    UPDATE lotes
    SET cantidad_actual = cantidad_actual - p_cantidad,
        peso_kg_actual = peso_kg_actual - p_peso_kg
    WHERE id = p_lote_id;

    INSERT INTO detalle_entrega(
        entrega_id,
        lote_id,
        cantidad,
        peso_kg,
        fecha_creacion
    )
    VALUES(
        p_entrega_id,
        p_lote_id,
        p_cantidad,
        p_peso_kg,
        p_fecha
    );

    INSERT INTO movimientos_inventario(
        lote_id,
        tipo_movimiento,
        referencia_tipo,
        referencia_id,
        cantidad,
        peso_kg,
        fecha_creacion
    )
    VALUES(
        p_lote_id,
        'SALIDA',
        'ENTREGA',
        p_entrega_id,
        p_cantidad,
        p_peso_kg,
        p_fecha
    );
END$$

CREATE PROCEDURE sp_get_inventario_vigente()
BEGIN
    SELECT
        l.id AS lote_id,
        l.codigo AS lote,
        p.nombre AS producto,
        c.nombre AS categoria,
        l.cantidad_actual,
        l.peso_kg_actual,
        l.fecha_vencimiento
    FROM lotes l
    INNER JOIN productos p ON p.id = l.producto_id
    INNER JOIN categorias_alimento c ON c.id = p.categoria_id
    WHERE l.cantidad_actual > 0
    ORDER BY l.fecha_vencimiento ASC;
END$$

CREATE PROCEDURE sp_get_lotes_por_vencer(
    IN p_dias INT
)
BEGIN
    SELECT
        l.id AS lote_id,
        l.codigo AS lote,
        p.nombre AS producto,
        l.fecha_vencimiento,
        l.cantidad_actual,
        DATEDIFF(l.fecha_vencimiento, CURDATE()) AS dias_restantes
    FROM lotes l
    INNER JOIN productos p ON p.id = l.producto_id
    WHERE l.cantidad_actual > 0
      AND l.fecha_vencimiento IS NOT NULL
      AND l.fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL p_dias DAY)
    ORDER BY l.fecha_vencimiento ASC;
END$$

CREATE PROCEDURE sp_get_trazabilidad_lote(
    IN p_lote_id INT
)
BEGIN
    SELECT
        l.id AS lote_id,
        l.codigo AS lote,
        p.nombre AS producto,
        d.id AS donacion_id,
        dn.nombre AS donante,
        e.id AS entrega_id,
        e.beneficiario,
        m.tipo_movimiento,
        m.referencia_tipo,
        m.referencia_id,
        m.cantidad,
        m.peso_kg,
        m.fecha_creacion
    FROM lotes l
    INNER JOIN productos p ON p.id = l.producto_id
    INNER JOIN donaciones d ON d.id = l.donacion_id
    INNER JOIN donantes dn ON dn.id = d.donante_id
    INNER JOIN movimientos_inventario m ON m.lote_id = l.id
    LEFT JOIN entregas e ON e.id = CASE WHEN m.referencia_tipo = 'ENTREGA' THEN m.referencia_id ELSE NULL END
    WHERE l.id = p_lote_id
    ORDER BY m.fecha_creacion ASC;
END$$

DELIMITER ;
