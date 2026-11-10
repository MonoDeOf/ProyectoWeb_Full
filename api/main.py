from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import carrito, favoritos, pedidos, productos, usuarios

# API única de Infraganti: antes eran dos (productos en 8000 y usuarios en 8001).
# Organización: routers (rutas HTTP), schemas (validación Pydantic),
# services (reglas de negocio y acceso a PostgreSQL) y database.py (conexiones).
app = FastAPI(title="API Infraganti")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(favoritos.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Estado"])
def inicio():
    return {"mensaje": "API de Infraganti funciona"}