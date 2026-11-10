from fastapi import APIRouter, Header

from schemas.usuario import LoginEntrada, RegistroEntrada
from services import usuarios_service

router = APIRouter(tags=["Usuarios"])


@router.post("/login")
def iniciar_sesion(datos: LoginEntrada):
    return usuarios_service.iniciar_sesion(datos.nick, datos.contrasena)


@router.post("/registro", status_code=201)
def registrar_usuario(datos: RegistroEntrada):
    return usuarios_service.registrar_usuario(datos)


@router.get("/perfil")
def obtener_perfil(x_usuario: str = Header(default=None)):
    return usuarios_service.obtener_perfil(x_usuario)
