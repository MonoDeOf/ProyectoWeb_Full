from fastapi import APIRouter, Header

from schemas.pedido import EstadoPedidoEntrada, PagoEntrada
from services import pedidos_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("")
def listar_pedidos(x_usuario: str = Header(default=None)):
    return pedidos_service.listar_pedidos(x_usuario)


@router.get("/{pedido_id}")
def obtener_pedido(pedido_id: int, x_usuario: str = Header(default=None)):
    return pedidos_service.obtener_pedido(pedido_id, x_usuario)


@router.post("", status_code=201)
def crear_pedido(x_usuario: str = Header(default=None)):
    return pedidos_service.crear_pedido(x_usuario)


@router.post("/{pedido_id}/pagar")
def pagar_pedido(
    pedido_id: int,
    datos: PagoEntrada = PagoEntrada(),
    x_usuario: str = Header(default=None),
):
    return pedidos_service.pagar_pedido(pedido_id, datos.metodo, x_usuario)


@router.patch("/{pedido_id}/estado")
def cambiar_estado(
    pedido_id: int,
    datos: EstadoPedidoEntrada,
    x_usuario: str = Header(default=None),
):
    return pedidos_service.cambiar_estado_pedido(pedido_id, datos.estado, x_usuario)