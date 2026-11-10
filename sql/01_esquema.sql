-- =====================================================================
-- INFRAGANTI MARKETPLACE · Hito 3 · Esquema PostgreSQL
-- Persistencia SQL obligatoria del caso 3.4 (Marketplace universitario):
-- usuarios, productos, categorías, pedidos y detalles.
-- Se agregan favoritos, carrito y transacciones simuladas porque son
-- funcionalidades obligatorias de expansión del caso.
--
-- Uso: psql -U <usuario> -d infraganti -f sql/01_esquema.sql
-- El script es repetible: elimina y vuelve a crear las tablas.
-- =====================================================================

-- pgcrypto permite guardar contraseñas cifradas (bcrypt) en vez de texto plano.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS transacciones   CASCADE;
DROP TABLE IF EXISTS detalle_pedido  CASCADE;
DROP TABLE IF EXISTS pedidos         CASCADE;
DROP TABLE IF EXISTS carrito_items   CASCADE;
DROP TABLE IF EXISTS favoritos       CASCADE;
DROP TABLE IF EXISTS productos       CASCADE;
DROP TABLE IF EXISTS categorias      CASCADE;
DROP TABLE IF EXISTS usuarios        CASCADE;

-- ---------------------------------------------------------------------
-- USUARIOS
-- Reemplaza api/usuarios.json. Conserva nick y rol (usuario / admin).
-- Un mismo usuario puede ser comprador y vendedor: el perfil vendedor
-- se da al publicar productos y el perfil comprador al crear pedidos.
-- ---------------------------------------------------------------------
CREATE TABLE usuarios (
    id               SERIAL       PRIMARY KEY,
    nick             VARCHAR(30)  NOT NULL UNIQUE CHECK (char_length(nick) >= 3),
    contrasena_hash  TEXT         NOT NULL,
    nombre           VARCHAR(60)  NOT NULL CHECK (char_length(nombre) >= 3),
    carrera          VARCHAR(60)  NOT NULL CHECK (char_length(carrera) >= 3),
    rol              VARCHAR(10)  NOT NULL DEFAULT 'usuario'
                                  CHECK (rol IN ('usuario', 'admin')),
    creado_en        TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- CATEGORÍAS
-- Reemplaza el arreglo CATEGORIAS de src/js/formato.js.
-- "slug" mantiene los mismos identificadores que usa React (libros, ...).
-- ---------------------------------------------------------------------
CREATE TABLE categorias (
    id      SERIAL       PRIMARY KEY,
    slug    VARCHAR(30)  NOT NULL UNIQUE,
    nombre  VARCHAR(40)  NOT NULL
);

-- ---------------------------------------------------------------------
-- PRODUCTOS
-- Reemplaza api/data.json. Mantiene las mismas reglas de ProductoEntrada
-- (api/main.py) y del formulario Publicar.jsx.
-- "carrera" se obtiene del usuario vendedor. "vendedor_nombre" guarda el
-- nombre que la persona escribe al publicar; si queda vacío se usa el de la cuenta.
-- "contacto" se conserva con su significado actual: lugar de entrega.
-- ---------------------------------------------------------------------
CREATE TABLE productos (
    id            SERIAL        PRIMARY KEY,
    vendedor_id   INTEGER       NOT NULL REFERENCES usuarios(id)   ON DELETE RESTRICT,
    categoria_id  INTEGER       NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    nombre        VARCHAR(80)   NOT NULL CHECK (char_length(nombre) >= 5),
    descripcion   VARCHAR(300)  NOT NULL CHECK (char_length(descripcion) >= 20),
    precio        INTEGER       NOT NULL CHECK (precio > 0 AND precio <= 10000000),
    estado        VARCHAR(12)   NOT NULL DEFAULT 'disponible'
                                CHECK (estado IN ('disponible', 'vendido')),
    contacto      VARCHAR(60)   NOT NULL CHECK (char_length(contacto) >= 3),
    vendedor_nombre VARCHAR(60) CHECK (char_length(vendedor_nombre) >= 3),
    imagen        TEXT          NOT NULL DEFAULT '',
    creado_en     TIMESTAMPTZ   NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ  NOT NULL DEFAULT now()
);


-- ---------------------------------------------------------------------
-- FAVORITOS (antes en localStorage: infraganti-favoritos)
-- ---------------------------------------------------------------------
CREATE TABLE favoritos (
    usuario_id   INTEGER      NOT NULL REFERENCES usuarios(id)  ON DELETE CASCADE,
    producto_id  INTEGER      NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    creado_en    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (usuario_id, producto_id)
);

-- ---------------------------------------------------------------------
-- CARRITO (antes en localStorage: infraganti-carrito)
-- Productos usados: cada artículo es único, por eso no hay cantidad.
-- ---------------------------------------------------------------------
CREATE TABLE carrito_items (
    usuario_id   INTEGER      NOT NULL REFERENCES usuarios(id)  ON DELETE CASCADE,
    producto_id  INTEGER      NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    agregado_en  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (usuario_id, producto_id)
);

-- ---------------------------------------------------------------------
-- PEDIDOS: creación y seguimiento por estado
-- ---------------------------------------------------------------------
CREATE TABLE pedidos (
    id              SERIAL       PRIMARY KEY,
    comprador_id    INTEGER      NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
    estado          VARCHAR(12)  NOT NULL DEFAULT 'pendiente'
                                 CHECK (estado IN ('pendiente', 'pagado', 'entregado', 'cancelado')),
    total           INTEGER      NOT NULL CHECK (total >= 0),
    creado_en       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    actualizado_en  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- DETALLE DEL PEDIDO
-- precio_unitario guarda el precio al momento de comprar, aunque el
-- producto cambie después.
-- ---------------------------------------------------------------------
CREATE TABLE detalle_pedido (
    id               SERIAL   PRIMARY KEY,
    pedido_id        INTEGER  NOT NULL REFERENCES pedidos(id)   ON DELETE CASCADE,
    producto_id      INTEGER  NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    precio_unitario  INTEGER  NOT NULL CHECK (precio_unitario > 0),
    UNIQUE (pedido_id, producto_id)
);

-- ---------------------------------------------------------------------
-- TRANSACCIONES SIMULADAS (no hay pagos reales, según el enunciado)
-- ---------------------------------------------------------------------
CREATE TABLE transacciones (
    id         SERIAL       PRIMARY KEY,
    pedido_id  INTEGER      NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    monto      INTEGER      NOT NULL CHECK (monto > 0),
    metodo     VARCHAR(20)  NOT NULL DEFAULT 'simulado'
                            CHECK (metodo IN ('simulado', 'transferencia', 'efectivo')),
    estado     VARCHAR(12)  NOT NULL CHECK (estado IN ('aprobada', 'rechazada')),
    creado_en  TIMESTAMPTZ  NOT NULL DEFAULT now()
);
