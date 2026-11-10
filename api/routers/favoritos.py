from fastapi import APIRouter, Header

from services import favoritos_service

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])


@router.get("")
def listar_favoritos(x_usuario: str = Header(default=None)):
    return favoritos_service.listar_favoritos(x_usuario)


@router.post("/{producto_id}", status_code=201)
def agregar_favorito(producto_id: int, x_usuario: str = Header(default=None)):
    return favoritos_service.agregar_favorito(producto_id, x_usuario)


@router.delete("/{producto_id}")
def quitar_favorito(producto_id: int, x_usuario: str = Header(default=None)):
    return favoritos_service.quitar_favorito(producto_id, x_usuario)
