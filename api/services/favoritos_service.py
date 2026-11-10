from fastapi import HTTPException

from database import conectar
from services.productos_service import buscar_datos_basicos
from services.usuarios_service import obtener_usuario


def es_favorito(cursor, usuario_id, producto_id):
    cursor.execute(
        "SELECT producto_id FROM favoritos WHERE usuario_id = %s AND producto_id = %s",
        (usuario_id, producto_id),
    )
    return cursor.fetchone() is not None


def listar_favoritos(nick):
    # Devuelve solo los ids, igual que el arreglo que usaba React
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT producto_id FROM favoritos WHERE usuario_id = %s ORDER BY creado_en",
        (usuario["id"],),
    )
    filas = cursor.fetchall()
    conexion.close()
    return [fila["producto_id"] for fila in filas]


def agregar_favorito(producto_id, nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()

    if buscar_datos_basicos(cursor, producto_id) is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Si ya estaba en favoritos no se repite, y la respuesta es la misma
    if not es_favorito(cursor, usuario["id"], producto_id):
        cursor.execute(
            "INSERT INTO favoritos (usuario_id, producto_id) VALUES (%s, %s)",
            (usuario["id"], producto_id),
        )
        conexion.commit()

    conexion.close()
    return {"mensaje": "Agregado a favoritos"}


def quitar_favorito(producto_id, nick):
    usuario = obtener_usuario(nick)

    conexion = conectar()
    cursor = conexion.cursor()

    if not es_favorito(cursor, usuario["id"], producto_id):
        conexion.close()
        raise HTTPException(status_code=404, detail="El producto no está en favoritos")

    cursor.execute(
        "DELETE FROM favoritos WHERE usuario_id = %s AND producto_id = %s",
        (usuario["id"], producto_id),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Quitado de favoritos"}