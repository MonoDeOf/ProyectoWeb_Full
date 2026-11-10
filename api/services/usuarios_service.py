from fastapi import HTTPException

from database import conectar

LETRAS_PERMITIDAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_."


def obtener_usuario(nick):
    # React envía el nick de la sesión en el encabezado X-Usuario
    # (igual que itemsApi.js del material envía X-DB-Provider).
    if not nick:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nick, rol FROM usuarios WHERE nick = %s", (nick,))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no válido")
    return usuario


def iniciar_sesion(nick, contrasena):
    # La contraseña se compara contra el hash guardado (bcrypt con pgcrypto),
    # nunca en texto plano.
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT nick, rol, nombre, carrera FROM usuarios
        WHERE nick = %s AND contrasena_hash = crypt(%s, contrasena_hash)
        """,
        (nick, contrasena),
    )
    usuario = cursor.fetchone()
    conexion.close()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Nick o contraseña incorrectos")
    return usuario


def registrar_usuario(datos):
    nombre = datos.nombre.strip()
    carrera = datos.carrera.strip()

    # Reglas de la cuenta
    for letra in datos.nick:
        if letra not in LETRAS_PERMITIDAS:
            raise HTTPException(
                status_code=400,
                detail="El nick solo puede tener letras, números, punto o guion bajo, sin espacios",
            )

    if len(nombre) < 3 or len(carrera) < 3:
        raise HTTPException(status_code=400, detail="Los datos de la cuenta no son válidos")

    conexion = conectar()
    cursor = conexion.cursor()

    # Regla: el nick no se puede repetir
    cursor.execute("SELECT id FROM usuarios WHERE nick = %s", (datos.nick,))
    if cursor.fetchone() is not None:
        conexion.close()
        raise HTTPException(status_code=409, detail="Ese nick ya está en uso. Elige otro.")

    # Las cuentas nuevas siempre son de rol "usuario"; la contraseña se guarda cifrada.
    cursor.execute(
        """
        INSERT INTO usuarios (nick, contrasena_hash, nombre, carrera, rol)
        VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s, 'usuario')
        """,
        (datos.nick, datos.contrasena, nombre, carrera),
    )
    conexion.commit()
    conexion.close()

    return {"nick": datos.nick, "rol": "usuario", "nombre": nombre, "carrera": carrera}


def obtener_perfil(nick):
    # Datos de la cuenta + resumen + ventas (productos propios que están en un pedido)
    # + compras (pedidos hechos por la cuenta)
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nick, nombre, carrera, rol, creado_en FROM usuarios WHERE id = %s",
        (usuario["id"],),
    )
    datos = cursor.fetchone()

    cursor.execute("SELECT estado FROM productos WHERE vendedor_id = %s", (usuario["id"],))
    publicaciones = cursor.fetchall()

    cursor.execute(
        """
        SELECT pe.id AS pedido_id, pe.estado, pe.creado_en,
               p.id AS producto_id, p.nombre, p.imagen, d.precio_unitario AS precio,
               c.nombre AS comprador
        FROM detalle_pedido d
        JOIN pedidos   pe ON pe.id = d.pedido_id
        JOIN productos p  ON p.id = d.producto_id
        JOIN usuarios  c  ON c.id = pe.comprador_id
        WHERE p.vendedor_id = %s
        ORDER BY pe.creado_en DESC, d.id
        """,
        (usuario["id"],),
    )
    ventas = cursor.fetchall()

    cursor.execute(
        """
        SELECT id, estado, total, creado_en FROM pedidos
        WHERE comprador_id = %s
        ORDER BY creado_en DESC
        """,
        (usuario["id"],),
    )
    compras = cursor.fetchall()

    # A cada compra se le agregan sus productos: cantidad, nombres e imagen del primero
    for compra in compras:
        cursor.execute(
            """
            SELECT p.nombre, p.imagen FROM detalle_pedido d
            JOIN productos p ON p.id = d.producto_id
            WHERE d.pedido_id = %s
            ORDER BY d.id
            """,
            (compra["id"],),
        )
        productos = cursor.fetchall()

        compra["cantidad_productos"] = len(productos)
        compra["productos"] = ", ".join([producto["nombre"] for producto in productos])
        compra["imagen"] = productos[0]["imagen"] if len(productos) > 0 else None

    conexion.close()

    # Las ventas y compras canceladas no suman al total
    disponibles = [producto for producto in publicaciones if producto["estado"] == "disponible"]
    ventas_validas = [venta for venta in ventas if venta["estado"] != "cancelado"]
    compras_validas = [compra for compra in compras if compra["estado"] != "cancelado"]

    total_vendido = 0
    for venta in ventas_validas:
        total_vendido = total_vendido + venta["precio"]

    total_comprado = 0
    for compra in compras_validas:
        total_comprado = total_comprado + compra["total"]

    return {
        "usuario": datos,
        "resumen": {
            "publicaciones": len(publicaciones),
            "disponibles": len(disponibles),
            "ventas": len(ventas_validas),
            "total_vendido": total_vendido,
            "compras": len(compras_validas),
            "total_comprado": total_comprado,
        },
        "ventas": ventas,
        "compras": compras,
    }