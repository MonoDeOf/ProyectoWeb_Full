from pydantic import BaseModel, Field


class PagoEntrada(BaseModel):
    # Pago simulado: no se procesa dinero real.
    # Los métodos permitidos se revisan en pedidos_service.py
    metodo: str = Field(default="simulado", max_length=20)


class EstadoPedidoEntrada(BaseModel):
    # Solo "cancelado" o "entregado". "pagado" se obtiene con POST /pedidos/{id}/pagar
    estado: str = Field(min_length=3, max_length=12)