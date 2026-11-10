from pydantic import BaseModel, Field


class LoginEntrada(BaseModel):
    nick: str = Field(min_length=3, max_length=30)
    contrasena: str = Field(min_length=3, max_length=60)


class RegistroEntrada(BaseModel):
    # Que el nick solo tenga letras, números, punto o guion bajo se revisa
    # en usuarios_service.py
    nick: str = Field(min_length=3, max_length=30)
    contrasena: str = Field(min_length=6, max_length=60)
    nombre: str = Field(min_length=3, max_length=60)
    carrera: str = Field(min_length=3, max_length=60)