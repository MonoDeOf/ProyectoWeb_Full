from fastapi import HTTPException

from database import conectar
from services.usuarios_service import obtener_usuario

# Consulta que une cada producto con su vendedor y su categoría
CONSULTA_PRODUCTOS = """
    SELECT p.id, p.nombre, c.slug AS categoria, p.estado, p.precio,
           p.descripcion, p.vendedor_nombre, u.nombre AS nombre_cuenta, u.carrera,
           p.contacto, p.imagen, u.nick AS vendedor_nick
    FROM productos p
    JOIN usuarios   u ON u.id = p.vendedor_id
    JOIN categorias c ON c.id = p.categoria_id
"""

ESTADOS_PRODUCTO = ["disponible", "vendido"]


def armar_producto(fila):
    # Devuelve el producto con el mismo formato que antes entregaba data.json.
    # "vendedor" es el nombre escrito al publicar; si no hay, el de la cuenta.
    vendedor = fila["vendedor_nombre"]
    if not vendedor:
        vendedor = fila["nombre_cuenta"]

    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "categoria": fila["categoria"],
        "estado": fila["estado"],
        "precio": fila["precio"],
        "descripcion": fila["descripcion"],
        "vendedor": vendedor,
        "carrera": fila["carrera"],
        "contacto": fila["contacto"],
        "imagen": fila["imagen"],
        "vendedor_nick": fila["vendedor_nick"],
    }


def buscar_producto(cursor, producto_id):
    # Devuelve el producto armado, o None si no existe
    cursor.execute(CONSULTA_PRODUCTOS + " WHERE p.id = %s", (producto_id,))
    fila = cursor.fetchone()

    if fila is None:
        return None
    return armar_producto(fila)


def buscar_datos_basicos(cursor, producto_id):
    # Dueño y estado del producto, o None si no existe
    cursor.execute("SELECT vendedor_id, estado FROM productos WHERE id = %s", (producto_id,))
    return cursor.fetchone()


def buscar_id_categoria(cursor, slug):
    # Id de la categoría, o None si no existe
    cursor.execute("SELECT id FROM categorias WHERE slug = %s", (slug,))
    fila = cursor.fetchone()

    if fila is None:
        return None
    return fila["id"]


def revisar_estado(estado):
    if estado not in ESTADOS_PRODUCTO:
        raise HTTPException(status_code=400, detail="El estado debe ser disponible o vendido")


def listar_categorias():
    # Mismo formato que usaba src/js/formato.js: { id, nombre }
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT slug AS id, nombre FROM categorias ORDER BY categorias.id")
    categorias = cursor.fetchall()
    conexion.close()
    return categorias


def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(CONSULTA_PRODUCTOS + " ORDER BY p.id")
    filas = cursor.fetchall()
    conexion.close()
    return [armar_producto(fila) for fila in filas]


def obtener_producto(producto_id):
    conexion = conectar()
    producto = buscar_producto(conexion.cursor(), producto_id)
    conexion.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def crear_producto(datos):
    revisar_estado(datos.estado)
    vendedor = datos.vendedor.strip()

    # Regla: solo se puede publicar a nombre de la propia cuenta
    if not datos.vendedor_nick:
        raise HTTPException(status_code=400, detail="Debes iniciar sesión para publicar")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE nick = %s", (datos.vendedor_nick,))
    cuenta = cursor.fetchone()
    if cuenta is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="El vendedor no tiene una cuenta registrada")

    categoria_id = buscar_id_categoria(cursor, datos.categoria)
    if categoria_id is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="Categoría no válida")

    if len(vendedor) < 3:
        conexion.close()
        raise HTTPException(status_code=400, detail="Los datos del producto no son válidos")

    # RETURNING id cumple el papel de cursor.lastrowid del taller con SQLite
    cursor.execute(
        """
        INSERT INTO productos
            (vendedor_id, categoria_id, nombre, descripcion, precio, estado, contacto,
             vendedor_nombre, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            cuenta["id"],
            categoria_id,
            datos.nombre,
            datos.descripcion,
            datos.precio,
            datos.estado,
            datos.contacto,
            vendedor,
            datos.imagen,
        ),
    )
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()

    producto = buscar_producto(cursor, nuevo_id)
    conexion.close()
    return producto


def actualizar_producto(producto_id, datos, nick):
    # El vendedor no cambia al editar: se conserva el dueño original.
    usuario = obtener_usuario(nick)
    revisar_estado(datos.estado)

    conexion = conectar()
    cursor = conexion.cursor()

    producto = buscar_datos_basicos(cursor, producto_id)
    if producto is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Regla: solo el dueño de la publicación o un administrador la modifica
    if producto["vendedor_id"] != usuario["id"] and usuario["rol"] != "admin":
        conexion.close()
        raise HTTPException(
            status_code=403,
            detail="Solo el vendedor o un administrador puede modificar esta publicación",
        )

    # Regla: un producto que está en un pedido activo no vuelve a estar disponible
    if datos.estado == "disponible" and producto["estado"] == "vendido":
        cursor.execute(
            """
            SELECT d.id FROM detalle_pedido d
            JOIN pedidos pe ON pe.id = d.pedido_id
            WHERE d.producto_id = %s AND pe.estado <> 'cancelado'
            """,
            (producto_id,),
        )
        if cursor.fetchone() is not None:
            conexion.close()
            raise HTTPException(
                status_code=409,
                detail="El producto pertenece a un pedido y no puede volver a estar disponible",
            )

    categoria_id = buscar_id_categoria(cursor, datos.categoria)
    if categoria_id is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="Categoría no válida")

    cursor.execute(
        """
        UPDATE productos
        SET categoria_id = %s, nombre = %s, descripcion = %s, precio = %s,
            estado = %s, contacto = %s, imagen = %s, actualizado_en = now()
        WHERE id = %s
        """,
        (
            categoria_id,
            datos.nombre,
            datos.descripcion,
            datos.precio,
            datos.estado,
            datos.contacto,
            datos.imagen,
            producto_id,
        ),
    )

    # Un producto vendido ya no puede seguir en el carrito de nadie
    if datos.estado == "vendido":
        cursor.execute("DELETE FROM carrito_items WHERE producto_id = %s", (producto_id,))

    conexion.commit()
    producto_actualizado = buscar_producto(cursor, producto_id)
    conexion.close()
    return producto_actualizado


def eliminar_producto(producto_id, nick):
    usuario = obtener_usuario(nick)

    # Regla: solo un administrador puede eliminar publicaciones
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo un administrador puede eliminar publicaciones")

    conexion = conectar()
    cursor = conexion.cursor()

    if buscar_datos_basicos(cursor, producto_id) is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Regla: un producto que forma parte de un pedido no se borra (se pierde el historial)
    cursor.execute("SELECT id FROM detalle_pedido WHERE producto_id = %s", (producto_id,))
    if cursor.fetchone() is not None:
        conexion.close()
        raise HTTPException(status_code=409, detail="El producto forma parte de un pedido y no se puede eliminar")

    # La base borra sola el producto de carritos y favoritos (ON DELETE CASCADE)
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "Producto eliminado"}