from fastapi import APIRouter, Header

from services import carrito_service

router = APIRouter(prefix="/carrito", tags=["Carrito"])


@router.get("")
def listar_carrito(x_usuario: str = Header(default=None)):
    return carrito_service.listar_carrito(x_usuario)


@router.post("/{producto_id}", status_code=201)
def agregar_al_carrito(producto_id: int, x_usuario: str = Header(default=None)):
    return carrito_service.agregar_al_carrito(producto_id, x_usuario)


@router.delete("/{producto_id}")
def quitar_del_carrito(producto_id: int, x_usuario: str = Header(default=None)):
    return carrito_service.quitar_del_carrito(producto_id, x_usuario)


@router.delete("")
def vaciar_carrito(x_usuario: str = Header(default=None)):
    return carrito_service.vaciar_carrito(x_usuario)