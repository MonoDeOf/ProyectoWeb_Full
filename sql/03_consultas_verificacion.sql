-- =====================================================================
-- INFRAGANTI MARKETPLACE · Consultas de verificación
-- Ejecutar después de 01_esquema.sql y 02_datos_prueba.sql.
-- =====================================================================

\dt

SELECT COUNT(*) AS total_usuarios   FROM usuarios;
SELECT COUNT(*) AS total_categorias FROM categorias;
SELECT COUNT(*) AS total_productos  FROM productos;

-- Productos con el mismo formato que hoy entrega GET /productos
SELECT p.id, p.nombre, c.slug AS categoria, p.estado, p.precio,
       u.nombre AS vendedor, u.carrera, p.contacto
FROM productos p
JOIN usuarios   u ON u.id = p.vendedor_id
JOIN categorias c ON c.id = p.categoria_id
ORDER BY p.id;

-- Login: la contraseña se compara contra el hash, nunca en texto plano
SELECT nick, rol FROM usuarios
WHERE nick = 'usuario' AND contrasena_hash = crypt('usuario123', contrasena_hash);

-- Pedidos con su detalle y sus pagos simulados (vacío hasta que alguien compre)
SELECT pe.id, pe.estado, pe.total, d.producto_id, d.precio_unitario
FROM pedidos pe
JOIN detalle_pedido d ON d.pedido_id = pe.id
ORDER BY pe.id;

SELECT id, pedido_id, monto, metodo, estado FROM transacciones ORDER BY id;
