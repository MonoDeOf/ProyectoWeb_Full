-- =====================================================================
-- INFRAGANTI MARKETPLACE · Datos de prueba
-- Origen: api/usuarios.json, api/data.json y src/js/formato.js.
-- Personas ficticias. Ejecutar después de 01_esquema.sql.
-- Contraseñas guardadas con bcrypt (pgcrypto), nunca en texto plano.
--   usuario / usuario123   · admin / admin123   (cuentas de prueba actuales)
--   vendedores de ejemplo / vendedor123
-- =====================================================================

INSERT INTO categorias (slug, nombre) VALUES
    ('libros',       'Libros'),
    ('computadores', 'Computadores'),
    ('accesorios',   'Accesorios'),
    ('instrumentos', 'Instrumentos'),
    ('deportes',     'Artículos deportivos'),
    ('otros',        'Otros productos');

INSERT INTO usuarios (nick, contrasena_hash, nombre, carrera, rol) VALUES
    ('usuario',   crypt('usuario123',  gen_salt('bf')), 'Usuario de prueba',  'Informática',      'usuario'),
    ('admin',     crypt('admin123',    gen_salt('bf')), 'Administrador',      'Informática',      'admin'),
    ('mrojas',    crypt('vendedor123', gen_salt('bf')), 'Matías Rojas',       'Ingeniería',       'usuario'),
    ('cperez',    crypt('vendedor123', gen_salt('bf')), 'Camila Pérez',       'Ingeniería',       'usuario'),
    ('dgonzalez', crypt('vendedor123', gen_salt('bf')), 'Diego González',     'Informática',      'usuario'),
    ('vsoto',     crypt('vendedor123', gen_salt('bf')), 'Valentina Soto',     'Diseño',           'usuario'),
    ('smunoz',    crypt('vendedor123', gen_salt('bf')), 'Sebastián Muñoz',    'Arquitectura',     'usuario'),
    ('ftorres',   crypt('vendedor123', gen_salt('bf')), 'Felipe Torres',      'Educación Física', 'usuario'),
    ('jsilva',    crypt('vendedor123', gen_salt('bf')), 'Javiera Silva',      'Diseño',           'usuario'),
    ('nfuentes',  crypt('vendedor123', gen_salt('bf')), 'Nicolás Fuentes',    'Informática',      'usuario'),
    ('fdiaz',     crypt('vendedor123', gen_salt('bf')), 'Francisca Díaz',     'Administración',   'usuario');

-- Los 9 productos de api/data.json, en el mismo orden (ids 1 a 9).
-- vendedor_id y categoria_id corresponden a los ids creados arriba:
--   usuarios: 3 mrojas, 4 cperez, 5 dgonzalez, 6 vsoto, 7 smunoz, 8 ftorres, 9 jsilva, 10 nfuentes, 11 fdiaz
--   categorías: 1 libros, 2 computadores, 3 accesorios, 4 instrumentos, 5 deportes, 6 otros
INSERT INTO productos (vendedor_id, categoria_id, nombre, descripcion, precio, estado, contacto, imagen) VALUES
    (3,  6, 'Calculadora Científica Escolar 240',
        'Calculadora científica en buen estado, ideal para estudiantes de ingeniería.', 15000,
        'disponible', 'Campus Santiago', '/assets/images/products/calculadora.jpg'),
    (4,  1, 'Libro Cálculo I Universitario',
        'Libro de cálculo utilizado durante el primer año universitario. Buen estado.', 22000,
        'disponible', 'Campus Santiago', '/assets/images/products/calculo.jpg'),
    (5,  2, 'Notebook Lenovo Ideapad Slim 3',
        'Notebook para estudio y trabajo. Incluye cargador y se encuentra en buen estado.', 450000,
        'disponible', 'Campus Santiago', '/assets/images/products/notebook.jpg'),
    (6,  3, 'Audifonos Bluetooh Active Silence Studio',
        'Audífonos inalámbricos con estuche de carga y buena autonomía.', 25000,
        'disponible', 'Campus Santiago', '/assets/images/products/audifonos.jpg'),
    (7,  4, 'Guitarra Acústica Vizcaya Arcg44 Cuerdas De Nylon Sunburst',
        'Guitarra acústica ideal para principiantes. Incluye funda.', 85000,
        'disponible', 'Campus Santiago', '/assets/images/products/guitarra.jpg'),
    (8,  5, 'Balón De Futbol Dribbling Drb Prime N°5',
        'Balón de fútbol en buen estado para entrenamientos y partidos.', 12000,
        'disponible', 'Campus Santiago', '/assets/images/products/balon.jpg'),
    (9,  3, 'Mouse Inalámbrico Hp 150',
        'Mouse inalámbrico compacto y cómodo para estudiar o trabajar.', 10000,
        'disponible', 'Campus Santiago', '/assets/images/products/mouse.jpg'),
    (10, 1, 'Libro Programación Java',
        'Libro introductorio de programación en Java para estudiantes.', 18000,
        'disponible', 'Campus Santiago', '/assets/images/products/java.jpg'),
    (11, 6, 'Mochila Notebook Impermeable Antirrobo',
        'Mochila con compartimento para notebook y múltiples bolsillos.', 20000,
        'disponible', 'Campus Santiago', '/assets/images/products/mochila.jpg');