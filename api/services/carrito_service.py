from fastapi import HTTPException

from database import conectar
from services.productos_service import (
    CONSULTA_PRODUCTOS,
    armar_producto,
    buscar_datos_basicos,
    buscar_producto,
)
from services.usuarios_service import obtener_usuario


def esta_en_carrito(cursor, usuario_id, producto_id):
    cursor.execute(
        "SELECT producto_id FROM carrito_items WHERE usuario_id = %s AND producto_id = %s",
        (usuario_id, producto_id),
    )
    return cursor.fetchone() is not None


def listar_carrito(nick):
    # Devuelve los productos completos, igual que el carrito que usaba React
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        CONSULTA_PRODUCTOS
        + " JOIN carrito_items ci ON ci.producto_id = p.id"
        + " WHERE ci.usuario_id = %s ORDER BY ci.agregado_en",
        (usuario["id"],),
    )
    filas = cursor.fetchall()
    conexion.close()
    return [armar_producto(fila) for fila in filas]


def agregar_al_carrito(producto_id, nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()

    producto = buscar_datos_basicos(cursor, producto_id)
    if producto is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Reglas de negocio del carrito
    if producto["estado"] == "vendido":
        conexion.close()
        raise HTTPException(status_code=409, detail="Este producto ya fue vendido")
    if producto["vendedor_id"] == usuario["id"]:
        conexion.close()
        raise HTTPException(status_code=409, detail="No puedes comprar tu propio producto")
    if esta_en_carrito(cursor, usuario["id"], producto_id):
        conexion.close()
        raise HTTPException(status_code=409, detail="El producto ya está en tu carrito")

    cursor.execute(
        "INSERT INTO carrito_items (usuario_id, producto_id) VALUES (%s, %s)",
        (usuario["id"], producto_id),
    )
    conexion.commit()

    producto_agregado = buscar_producto(cursor, producto_id)
    conexion.close()
    return producto_agregado


def quitar_del_carrito(producto_id, nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()

    if not esta_en_carrito(cursor, usuario["id"], producto_id):
        conexion.close()
        raise HTTPException(status_code=404, detail="El producto no está en el carrito")

    cursor.execute(
        "DELETE FROM carrito_items WHERE usuario_id = %s AND producto_id = %s",
        (usuario["id"], producto_id),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Quitado del carrito"}


def vaciar_carrito(nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM carrito_items WHERE usuario_id = %s", (usuario["id"],))
    conexion.commit()
    conexion.close()
    return {"mensaje": "Carrito vaciado"}