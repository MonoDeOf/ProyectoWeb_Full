from fastapi import APIRouter, Header

from schemas.producto import ProductoEntrada
from services import productos_service

router = APIRouter(tags=["Productos y categorías"])


@router.get("/categorias")
def listar_categorias():
    return productos_service.listar_categorias()


@router.get("/productos")
def listar_productos():
    return productos_service.listar_productos()


@router.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    return productos_service.obtener_producto(producto_id)


@router.post("/productos", status_code=201)
def crear_producto(datos: ProductoEntrada):
    return productos_service.crear_producto(datos)


@router.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    x_usuario: str = Header(default=None),
):
    return productos_service.actualizar_producto(producto_id, datos, x_usuario)


@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, x_usuario: str = Header(default=None)):
    return productos_service.eliminar_producto(producto_id, x_usuario)