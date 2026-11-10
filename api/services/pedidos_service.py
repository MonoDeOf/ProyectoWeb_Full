from fastapi import HTTPException

from database import conectar
from services.usuarios_service import obtener_usuario

# Cambios de estado permitidos (pendiente -> pagado se hace con /pagar)
TRANSICIONES = {
    "pendiente": ["cancelado"],
    "pagado": ["entregado"],
}

METODOS_PAGO = ["simulado", "transferencia", "efectivo"]
ESTADOS_PERMITIDOS = ["cancelado", "entregado"]


def armar_pedido(cursor, pedido):
    # Agrega al pedido sus productos (detalle) y sus transacciones simuladas
    cursor.execute(
        """
        SELECT p.id, p.nombre, p.imagen, d.precio_unitario AS precio,
               p.vendedor_nombre, u.nombre AS nombre_cuenta
        FROM detalle_pedido d
        JOIN productos p ON p.id = d.producto_id
        JOIN usuarios  u ON u.id = p.vendedor_id
        WHERE d.pedido_id = %s
        ORDER BY d.id
        """,
        (pedido["id"],),
    )
    productos = []
    for fila in cursor.fetchall():
        # El vendedor es el nombre escrito al publicar; si no hay, el de la cuenta
        vendedor = fila["vendedor_nombre"]
        if not vendedor:
            vendedor = fila["nombre_cuenta"]

        productos.append({
            "id": fila["id"],
            "nombre": fila["nombre"],
            "imagen": fila["imagen"],
            "precio": fila["precio"],
            "vendedor": vendedor,
        })
    pedido["productos"] = productos

    cursor.execute(
        """
        SELECT id, monto, metodo, estado, creado_en
        FROM transacciones WHERE pedido_id = %s ORDER BY id
        """,
        (pedido["id"],),
    )
    pedido["transacciones"] = cursor.fetchall()
    return pedido


def buscar_pedido(cursor, pedido_id):
    cursor.execute(
        """
        SELECT id, comprador_id, estado, total, creado_en, actualizado_en
        FROM pedidos WHERE id = %s
        """,
        (pedido_id,),
    )
    return cursor.fetchone()


def revisar_pedido(conexion, pedido, usuario):
    # Si el pedido no existe o no es de la cuenta, cierra la conexión y avisa
    if pedido is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido["comprador_id"] != usuario["id"] and usuario["rol"] != "admin":
        conexion.close()
        raise HTTPException(status_code=403, detail="Este pedido no te pertenece")


def listar_pedidos(nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id, comprador_id, estado, total, creado_en, actualizado_en
        FROM pedidos WHERE comprador_id = %s
        ORDER BY creado_en DESC
        """,
        (usuario["id"],),
    )
    pedidos = [armar_pedido(cursor, pedido) for pedido in cursor.fetchall()]
    conexion.close()
    return pedidos


def obtener_pedido(pedido_id, nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    pedido = buscar_pedido(cursor, pedido_id)
    revisar_pedido(conexion, pedido, usuario)

    pedido = armar_pedido(cursor, pedido)
    conexion.close()
    return pedido


def crear_pedido(nick):
    # Crea el pedido con todo lo que el usuario tiene en su carrito.
    # Si algo falla antes del commit, se cierra la conexión sin guardar nada.
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT p.id, p.nombre, p.precio, p.estado, p.vendedor_id
        FROM carrito_items ci
        JOIN productos p ON p.id = ci.producto_id
        WHERE ci.usuario_id = %s
        ORDER BY ci.agregado_en
        """,
        (usuario["id"],),
    )
    productos = cursor.fetchall()

    # Reglas de negocio del pedido
    if len(productos) == 0:
        conexion.close()
        raise HTTPException(status_code=400, detail="Tu carrito está vacío")

    total = 0
    for producto in productos:
        if producto["estado"] == "vendido":
            conexion.close()
            raise HTTPException(status_code=409, detail=f"«{producto['nombre']}» ya fue vendido")
        if producto["vendedor_id"] == usuario["id"]:
            conexion.close()
            raise HTTPException(status_code=409, detail="No puedes comprar tu propio producto")
        total = total + producto["precio"]

    cursor.execute(
        "INSERT INTO pedidos (comprador_id, total) VALUES (%s, %s) RETURNING id",
        (usuario["id"], total),
    )
    pedido_id = cursor.fetchone()["id"]

    for producto in productos:
        cursor.execute(
            "INSERT INTO detalle_pedido (pedido_id, producto_id, precio_unitario) VALUES (%s, %s, %s)",
            (pedido_id, producto["id"], producto["precio"]),
        )

        # El producto queda reservado (vendido) solo si sigue disponible.
        # Si otra persona lo compró justo antes, no se guarda nada del pedido.
        cursor.execute(
            """
            UPDATE productos SET estado = 'vendido', actualizado_en = now()
            WHERE id = %s AND estado = 'disponible'
            RETURNING id
            """,
            (producto["id"],),
        )
        if cursor.fetchone() is None:
            conexion.close()
            raise HTTPException(status_code=409, detail=f"«{producto['nombre']}» ya fue vendido")

        # Un producto vendido sale de todos los carritos
        cursor.execute("DELETE FROM carrito_items WHERE producto_id = %s", (producto["id"],))

    conexion.commit()

    pedido = armar_pedido(cursor, buscar_pedido(cursor, pedido_id))
    conexion.close()
    return pedido


def pagar_pedido(pedido_id, metodo, nick):
    # Transacción simulada: no se procesa dinero real
    usuario = obtener_usuario(nick)

    if metodo not in METODOS_PAGO:
        raise HTTPException(status_code=400, detail="El método de pago debe ser simulado, transferencia o efectivo")

    conexion = conectar()
    cursor = conexion.cursor()
    pedido = buscar_pedido(cursor, pedido_id)
    revisar_pedido(conexion, pedido, usuario)

    # Solo cambia si sigue pendiente; así no se puede pagar dos veces
    cursor.execute(
        """
        UPDATE pedidos SET estado = 'pagado', actualizado_en = now()
        WHERE id = %s AND estado = 'pendiente'
        RETURNING id
        """,
        (pedido_id,),
    )
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=409, detail="Solo se puede pagar un pedido pendiente")

    cursor.execute(
        "INSERT INTO transacciones (pedido_id, monto, metodo, estado) VALUES (%s, %s, %s, 'aprobada')",
        (pedido_id, pedido["total"], metodo),
    )
    conexion.commit()

    pedido = armar_pedido(cursor, buscar_pedido(cursor, pedido_id))
    conexion.close()
    return pedido


def cambiar_estado_pedido(pedido_id, nuevo_estado, nick):
    usuario = obtener_usuario(nick)

    if nuevo_estado not in ESTADOS_PERMITIDOS:
        raise HTTPException(status_code=400, detail="El estado debe ser cancelado o entregado")

    conexion = conectar()
    cursor = conexion.cursor()
    pedido = buscar_pedido(cursor, pedido_id)
    revisar_pedido(conexion, pedido, usuario)

    estado_actual = pedido["estado"]
    permitidos = []
    if estado_actual in TRANSICIONES:
        permitidos = TRANSICIONES[estado_actual]

    if nuevo_estado not in permitidos:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail=f"Un pedido {estado_actual} no puede pasar a {nuevo_estado}",
        )

    # Solo cambia si el estado no fue modificado por otra petición entre medio
    cursor.execute(
        """
        UPDATE pedidos SET estado = %s, actualizado_en = now()
        WHERE id = %s AND estado = %s
        RETURNING id
        """,
        (nuevo_estado, pedido_id, estado_actual),
    )
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=409, detail="El pedido cambió de estado. Recarga la página.")

    # Al cancelar, los productos vuelven a estar disponibles en el Mercado
    if nuevo_estado == "cancelado":
        cursor.execute("SELECT producto_id FROM detalle_pedido WHERE pedido_id = %s", (pedido_id,))
        for fila in cursor.fetchall():
            cursor.execute(
                "UPDATE productos SET estado = 'disponible', actualizado_en = now() WHERE id = %s",
                (fila["producto_id"],),
            )

    conexion.commit()

    pedido = armar_pedido(cursor, buscar_pedido(cursor, pedido_id))
    conexion.close()
    return pedido