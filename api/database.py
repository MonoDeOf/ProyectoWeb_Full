import os

import psycopg
from psycopg.rows import dict_row

# Igual que database.py del taller de FastAPI (Semana 8), pero con PostgreSQL
# en vez de SQLite, porque el enunciado del Hito 3 exige PostgreSQL.
# La dirección de la base se lee desde una variable de entorno, para no
# dejar credenciales en el código. Ver .env.example.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://127.0.0.1:5432/infraganti")


def conectar():
    # dict_row cumple el mismo papel que sqlite3.Row en el taller:
    # cada fila se puede leer como fila["nombre"].
    # connect_timeout evita que la API se quede esperando si la base no responde.
    return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=5)