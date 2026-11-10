from pydantic import BaseModel, Field


class ProductoEntrada(BaseModel):
    nombre: str = Field(min_length=5, max_length=80)
    categoria: str = Field(min_length=3, max_length=30)
    # "disponible" o "vendido": se revisa en productos_service.py
    estado: str = "disponible"
    precio: int = Field(gt=0, le=10000000)
    descripcion: str = Field(min_length=20, max_length=300)
    vendedor: str = Field(min_length=3, max_length=60)
    carrera: str = Field(min_length=3, max_length=60)
    contacto: str = Field(min_length=3, max_length=60)
    imagen: str = ""
    # Nick de la cuenta con la sesión iniciada. Obligatorio al publicar (POST).
    vendedor_nick: str = ""