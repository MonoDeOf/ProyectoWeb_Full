# INFRAGANTI MARKETPLACE

Plataforma web de compra y venta de productos entre estudiantes de la comunidad universitaria. Permite publicar artículos (libros, computadores, accesorios, instrumentos, artículos deportivos y otros), explorarlos con filtros, ver su detalle y gestionar su estado de venta, con vistas diferenciadas según el rol de quien navega.

El proyecto se compone de un **frontend en React** y **dos APIs REST en FastAPI** (una de productos y otra de usuarios/autenticación).

## Integrantes

| Nombre | 
| ----- | 
| Benjamin Farias | 
| Benjamin Villarroel | 
| Omar Millar | 
| Frank Häfelin | 

## Contenido

 1. Descripción de la problemática y Diagnóstico del Taller 2

 2. Usuarios objetivo e Historias de Usuario

 3. Funcionalidades principales

 4. Tecnologías

 5. Estructura del proyecto, Arquitectura y Navegación

 6. API pública utilizada y documentación oficial

 7. Endpoints utilizados

 8. Justificación funcional de la API y Modelado de Datos (SQL/NoSQL)

 9. Diseño de la plataforma

10. Flujo de la plataforma

11. Criterio de coherencia

12. Instalación, ejecución y despliegue con Docker

13. Persistencia de datos

14. Pruebas

15. Limitaciones conocidas

16. Uso de Inteligencia Artificial

17. Cuentas de prueba

18. Solución de problemas

19. Mejoras futuras

## Descripción de la problemática y Diagnóstico del Taller 2

Dentro de la comunidad universitaria, los estudiantes compran y venden con frecuencia libros, computadores, accesorios, instrumentos y artículos deportivos. Hoy esa actividad ocurre en canales informales (grupos de mensajería, redes sociales y avisos sueltos), donde **no existe una plataforma de confianza** pensada para realizar compras y ventas de artículos entre estudiantes.

Esa falta de una plataforma confiable genera problemas concretos:

* **Desconfianza entre las partes:** no hay una forma clara de saber quién publica, de qué carrera es ni cómo contactarlo, lo que facilita estafas y publicaciones engañosas.

* **Información dispersa y sin estructura:** cada aviso describe el producto a su manera, sin precio, estado, categoría o lugar de entrega ordenados.

* **Publicaciones desactualizadas:** artículos ya vendidos siguen apareciendo como disponibles, y los interesados pierden tiempo preguntando por ellos.

* **Dificultad para encontrar lo que se busca:** sin búsqueda ni filtros, ubicar un producto exige revisar largas conversaciones.

* **Sin control ni moderación:** nadie puede retirar publicaciones inadecuadas ni evitar el spam.

**INFRAGANTI MARKETPLACE** busca responder a este problema ofreciendo un espacio único y ordenado para la comunidad estudiantil, con:

* Publicaciones **estructuradas** (precio, categoría, estado, descripción, vendedor, carrera, contacto y lugar de entrega).

* **Estado visible** de cada artículo (Disponible o Vendido).

* **Acceso con sesión** para comprar y publicar, con roles de usuario y administrador.

* **Moderación** a cargo del administrador, que puede eliminar publicaciones, y una **espera de 30 segundos** entre publicaciones para limitar el spam.

* **Información verificable de libros** mediante la API pública de Open Library, que ayuda al comprador a confirmar que el título, autor y edición corresponden a lo ofrecido.

### Diagnóstico del Taller 2 (Continuidad de Etapa 1)

El presente desarrollo evidencia una clara evolución sobre el caso planteado en el Taller 2:

* **Qué se conserva:** El dominio central del problema (marketplace universitario), los tipos de artículos, la necesidad de estructurar publicaciones y los roles base.

* **Qué se modifica:** La arquitectura pasa de un esquema puramente local/estático a una estructura robusta cliente-servidor, migrando a bases de datos reales para asegurar la integridad de la información y la concurrencia.

* **Qué se amplía:** Se incorporan flujos end-to-end completos (carrito, checkout simulado de pedidos), persistencia avanzada mediante Docker (PostgreSQL para modelo relacional y MongoDB para interacciones de preguntas/respuestas), y validaciones exhaustivas de negocio.


## Usuarios objetivo e Historias de Usuario

| Usuario | Necesidad | 
| ----- | ----- | 
| **Estudiantes compradores** | Encontrar artículos de segunda mano a buen precio, con información clara y de una fuente confiable. | 
| **Estudiantes vendedores** | Publicar sus artículos de forma ordenada y mantener actualizado su estado de venta. | 
| **Administradores o moderadores** | Supervisar el catálogo y retirar publicaciones inadecuadas. | 
| **Visitantes** | Explorar el catálogo antes de decidir si crear una sesión y participar. | 

### Historias de Usuario Principales

1. **Como estudiante comprador**, quiero filtrar los productos por categoría y rango de precio para encontrar rápidamente lo que necesito para mis estudios.

2. **Como estudiante vendedor**, quiero poder cambiar el estado de mi artículo a "Vendido" de forma sencilla para dejar de recibir consultas una vez que cerré el trato.

3. **Como usuario autenticado**, quiero poder dejar preguntas públicas en un producto y recibir respuestas del vendedor, para aclarar dudas antes de agregar el ítem al carrito.

4. **Como administrador**, quiero tener privilegios para eliminar cualquier publicación de la plataforma para mantener el orden y evitar contenido inapropiado o spam.

## Funcionalidades principales

* Catálogo con portada, productos *Nuevos* y *Populares por categoría*.

* Búsqueda por texto y filtros por categoría, estado y rango de precio, con orden por precio o nombre.

* Detalle del producto con recomendaciones de la misma categoría.

* Inicio y cierre de sesión con tres perfiles: visitante, usuario y administrador.

* Carrito de compra y favoritos (con sesión iniciada).

* Publicación de productos con validación de formulario y procesamiento de imagen.

* Cambio de estado Disponible/Vendido y eliminación de publicaciones (esta última solo para el administrador).

* Información de libros (autor, primera edición y portada) mediante Open Library.

* Persistencia de sesión, carrito y favoritos en el navegador.

## Tecnologías

| Capa | Tecnología | 
| ----- | ----- | 
| Frontend | React, Vite, JavaScript, Bootstrap 5.3.8 (CDN) y CSS por página | 
| Backend de productos | Python, FastAPI, Pydantic (puerto 8000) | 
| Backend de usuarios | Python, FastAPI, Pydantic (puerto 8001) | 
| Servicio externo | API pública de [Open Library](https://openlibrary.org) (información de libros) | 
| Base de Datos Relacional | PostgreSQL 16 (Usuarios, Productos, Pedidos, Carrito) | 
| Base de Datos Documental | MongoDB 8.0 (Preguntas y respuestas) | 
| Infraestructura | Docker y Docker Compose | 
| Datos de respaldo base | `api/data.json` y `api/usuarios.json` (cargados en memoria en versión local sin DB) | 
| Persistencia en el navegador | `localStorage` (sesión, carrito, favoritos y publicaciones propias) | 

## Estructura del proyecto, Arquitectura y Navegación

```
WebReact/
├── api/
│   ├── main.py              # API de productos (CRUD) — puerto 8000
│   ├── data.json            # 9 productos iniciales
│   ├── usuarios.py          # API de usuarios (login) — puerto 8001
│   └── usuarios.json        # Cuentas de prueba con su rol
├── mongo/
│   └── 01_preguntas.js      # Script de inicialización colección NoSQL
├── sql/
│   ├── 01_esquema.sql       # DDL y creación de tablas PostgreSQL
│   ├── 02_datos_prueba.sql  # Datos iniciales para SQL
│   └── 03_consultas_verificacion.sql
├── public/
│   └── assets/images/       # Logo, portada e imágenes de productos
├── src/
│   ├── App.jsx              # Estado global, sesión, llamadas a las APIs y navegación
│   ├── main.jsx             # Punto de entrada de React
│   ├── components/          # 16 componentes reutilizables
│   ├── pages/               # Inicio, Mercado, Producto, Publicar, Login, Pedidos, Perfil
│   ├── services/            # openLibrary.js y APIs propias
│   ├── js/                  # formato.js y almacenamiento.js
│   └── styles/              # Estilos globales y por página
├── compose.yaml             # Orquestación de contenedores (App, API, Postgres, Mongo)
├── Dockerfile               # Configuración de imagen de React
└── package.json             

```

### Diagrama de Arquitectura

La arquitectura del proyecto está estructurada en un modelo Cliente-Servidor orquestado completamente por Docker:

* El **Frontend** (React + Vite) expuesto en el puerto 5173 se comunica vía peticiones HTTP (fetch).

* El **Backend** cuenta con APIs en FastAPI que reciben las peticiones y aplican reglas de negocio.

* La **Persistencia** está dividida (Polyglot Persistence): PostgreSQL en el puerto 5432 maneja transacciones ACID (productos, usuarios, pedidos), mientras que MongoDB en el puerto 27018 maneja de forma documental las interacciones (preguntas).

### Mapa de Navegación

La experiencia de usuario sigue el siguiente flujo principal:

1. `Inicio`: Vista de aterrizaje y destacados.

2. `Mercado`: Exploración total con filtros combinados.

3. `Detalle de Producto`: Vista de información completa, conexión a Open Library y módulo de preguntas (Mongo).

4. (Requiere Login) `Carrito` -> `Pedidos` (Checkout y cambio de estados).

5. (Requiere Login) `Perfil` -> `Publicar Producto` o gestionar artículos propios.

## API pública utilizada y documentación oficial

El proyecto consume la API pública de **Open Library**, un servicio gratuito del Internet Archive con información bibliográfica de millones de libros. No requiere clave de acceso (API key) y se consulta directamente desde el frontend con `fetch`.

| Recurso | Dirección | 
| ----- | ----- | 
| Sitio oficial | https://openlibrary.org | 
| Documentación general de la API | https://openlibrary.org/developers/api | 
| Documentación de la API de búsqueda | https://openlibrary.org/dev/docs/api/search | 
| Documentación de la API de portadas | https://openlibrary.org/dev/docs/api/covers | 

Además, el proyecto expone sus **propias APIs** con FastAPI (productos y usuarios), descritas en [Criterio de coherencia](#criterio-de-coherencia-cambios-e-incrementos-realizados).

## Endpoints utilizados

### Open Library (API pública)

| Método | Endpoint | Parámetros | Uso en el proyecto | 
| ----- | ----- | ----- | ----- | 
| `GET` | `https://openlibrary.org/search.json` | `title` (título buscado) y `limit=3` | Busca libros por título. Se usan los campos `key`, `title`, `author_name`, `first_publish_year` y `cover_i`. | 
| `GET` | `https://covers.openlibrary.org/b/id/{cover_i}-M.jpg` | `cover_i` obtenido de la búsqueda | Entrega la portada en tamaño mediano. | 

Ejemplo de consulta:

```
https://openlibrary.org/search.json?title=el%20principito&limit=3

```

## Justificación funcional de la API y Modelado de Datos (SQL/NoSQL)

El problema central del proyecto es la **falta de confianza** al comprar y vender entre estudiantes. La API de Open Library aporta a resolverlo mediante la **verificación de la oferta**, información externa objetiva y menor carga para el vendedor.

### Tabla de Endpoints y Diseño API REST

Los endpoints fueron diseñados bajo principios RESTful, donde los recursos (`/productos`, `/usuarios`, `/pedidos`) están alineados directamente con las entidades del modelo relacional.

**API de Productos y Transacciones (Puerto 8000)**

| Método | Endpoint | Descripción | Requiere Sesión |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Verifica que el servicio esté activo. | No |
| `GET` | `/categorias` | Lista todas las categorías disponibles para el mercado. | No |
| `GET` | `/productos` | Lista todos los productos disponibles en el catálogo. | No |
| `GET` | `/productos/{id}` | Obtiene el detalle de un producto específico. | No |
| `POST` | `/productos` | Crea y publica un nuevo producto en el catálogo. | Sí |
| `PUT` | `/productos/{id}` | Actualiza un producto, como su estado (disponible/vendido). | Sí |
| `DELETE`| `/productos/{id}` | Elimina una publicación del sistema. | Sí (Admin/Dueño) |
| `GET` | `/usuarios/{nick}/carrito` | Obtiene los productos actuales en el carrito del usuario. | Sí |
| `POST` | `/usuarios/{nick}/carrito` | Agrega un producto (por ID) al carrito del usuario. | Sí |
| `DELETE`| `/usuarios/{nick}/carrito/{id}` | Elimina un producto específico del carrito. | Sí |
| `DELETE`| `/usuarios/{nick}/carrito` | Vacía completamente el carrito del usuario. | Sí |
| `GET` | `/usuarios/{nick}/favoritos` | Lista los IDs de los productos marcados como favoritos. | Sí |
| `POST` | `/usuarios/{nick}/favoritos` | Agrega un producto a la lista de favoritos. | Sí |
| `DELETE`| `/usuarios/{nick}/favoritos/{id}` | Quita un producto de la lista de favoritos. | Sí |
| `GET` | `/usuarios/{nick}/pedidos` | Lista el historial de pedidos del usuario. | Sí |
| `POST` | `/usuarios/{nick}/pedidos` | Crea un nuevo pedido a partir de los ítems en el carrito. | Sí |
| `POST` | `/pedidos/{id}/pagar` | Registra el pago simulado de un pedido específico. | Sí |
| `PUT` | `/pedidos/{id}/estado` | Cambia el estado operativo de un pedido (ej. entregado, cancelado). | Sí |

**API de Usuarios y Autenticación (Puerto 8001)**

| Método | Endpoint | Descripción | Requiere Sesión |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Verifica que el servicio de autenticación esté activo. | No |
| `POST` | `/login` | Valida las credenciales (`nick` y `contrasena`) y devuelve los datos de sesión y rol. | No |
| `POST` | `/registro` | Registra una nueva cuenta de usuario en el sistema. | No |
| `GET` | `/usuarios/{nick}/perfil` | Obtiene los datos del perfil de un usuario. | Sí |

### Modelo entidad-relación (SQL)

![Modelo Entidad-Relación](image_d698b8.jpg)

Para garantizar la consistencia, la trazabilidad de los pedidos y la gestión de usuarios, se implementó PostgreSQL con el siguiente esquema:

* **`usuarios`**: Almacena credenciales (con hash vía `pgcrypto`), nombre, carrera y rol.

* **`productos` y `categorias`**: El núcleo del catálogo, con referencias (FK) al vendedor.

* **`pedidos`, `detalle_pedido` y `transacciones`**: Gestión de la compra simulada, almacenando precios históricos para asegurar la inmutabilidad de la boleta.

* **`carrito_items` y `favoritos`**: Tablas asociativas que vinculan al usuario con el producto deseado.

### Diseño de la colección (NoSQL)

Se justificó el uso de MongoDB para la colección **`preguntas`** debido a su naturaleza orientada a documentos:

* **Patrón de acceso óptimo:** Cada pregunta se lee y se escribe completa con su respuesta embebida (nested object), evitando operaciones de JOIN costosas que serían requeridas en SQL.

* **Estructura ágil:** Mantiene referencias directas a `producto_id` y `vendedor_id` de PostgreSQL, pero encapsulando el hilo de conversación `texto` -> `respuesta.texto` de manera jerárquica y eficiente en formato BSON JSON-Schema.

## Diseño de la plataforma

La interfaz usa una barra de navegación superior con logo, buscador y accesos que **cambian según el rol**, diseño responsive con la grilla de Bootstrap y tarjetas de producto con indicador de estado (**Disponible** / **Vendido**). La plataforma maneja tres perfiles:

| Perfil | Cómo se accede | 
| ----- | ----- | 
| **Visitante** | Sin iniciar sesión | 
| **Usuario** | Inicio de sesión con rol `usuario` | 
| **Administrador** | Inicio de sesión con rol `admin` | 

*(El detalle completo de vistas está implementado en la aplicación, donde Administradores tienen facultades extendidas de moderación y eliminación sin cooldown de publicación).*

## Flujo de la plataforma

```
Inicio ---> Buscar ---> Ver detalles ---> Ejecutar acción ---> Confirmación ---> Actualización de estado

```

*(El flujo end-to-end soporta la navegación desde React hasta la persistencia y retorno de datos, con confirmaciones visuales para cada operación asíncrona).*

## Criterio de coherencia: cambios e incrementos realizados

### 1. División de vistas de administrador y usuario

Se incorporó un sistema de autenticación completo, validado localmente o mediante la base de datos en PostgreSQL (según el entorno de ejecución).

### 2. Implementación de la API mediante FastAPI

Se reemplazó el manejo local por servicios REST con validación estricta mediante modelos Pydantic.

### 3. Implementación de React y sus funcionalidades

Manejo de estado robusto con hooks, integración con Open Library, y arquitectura por componentes escalable.

## Instalación, ejecución y despliegue con Docker

### Opción 1: Ejecución con Docker Compose (Recomendada - Etapa 4)

Para reproducir la infraestructura real, incluyendo PostgreSQL y MongoDB, el proyecto está completamente dockerizado.
**Requisitos:** Tener Docker Desktop instalado y corriendo.

1. Clona el repositorio y sitúate en la raíz del proyecto.

2. Copia el archivo de variables de entorno:

   ```
   cp .env.example .env
   
   ```

3. Levanta los contenedores en segundo plano:

   ```
   docker compose up -d --build
   
   ```

*Nota: Los scripts `sql/01_esquema.sql`, `sql/02_datos_prueba.sql` y `mongo/01_preguntas.js` se ejecutarán automáticamente al crear los volúmenes, dejando el sistema listo para usar.*

**Accesos del entorno Docker:**

* Frontend React: `http://127.0.0.1:5173`

* Backend API: `http://127.0.0.1:8000`

* PostgreSQL: Puerto `5432`

* MongoDB: Puerto `27018`

### Opción 2: Ejecución Manual en Memoria (Prototipo Básico)

*(Instrucciones previas de desarrollo sin bases de datos)*
Si prefieres correrlo sin Docker usando los JSON de prueba:

1. Terminal 1 (API Productos): `cd api` -> `uvicorn main:app --reload --port 8000`

2. Terminal 2 (API Usuarios): `cd api` -> `uvicorn usuarios:app --reload --port 8001`

3. Terminal 3 (React Frontend): En la raíz -> `npm install` -> `npm run dev`

## Persistencia de datos

El proyecto contempla dos modalidades de persistencia, evolucionando desde la etapa inicial a la final:

1. **Persistencia mediante Bases de Datos (Entorno Docker):**

   * Todos los cambios de **Productos, Usuarios y Pedidos** se insertan y mantienen de manera inmutable en **PostgreSQL**, sobreviviendo a reinicios del servidor gracias a los volúmenes configurados (`postgres_infraganti`).

   * Las interacciones de **Preguntas** se mantienen en **MongoDB** (`mongo_infraganti`).

2. **Persistencia en Memoria y LocalStorage (Entorno Manual):**

   * Si se ejecuta el proyecto sin Docker, los datos se apoyan en `data.json` y se restablecen al reiniciar uvicorn. El carrito, favoritos y sesión se guardan en el `localStorage` del navegador.

## Pruebas

Se implementaron pruebas funcionales automatizadas que validan reglas de negocio, manejo de errores y cobertura de flujos relevantes de la API integrada.

**Cómo ejecutarla:** (Con la infraestructura Docker encendida)

```
npm run test:smoke

```

**Qué comprueba:**

* **Usuarios:** Registro, login, bloqueos por nick repetido (409) o contraseña inválida (401).

* **Productos (PostgreSQL):** CRUD, reglas de edición/eliminación solo para admin o dueño (403), validación de precio y catálogo.

* **Carritos/Pedidos:** Simulaciones de pago, bloqueos para comprar el propio producto, protección de pedidos ajenos y estados de cancelación.

* **Preguntas (MongoDB):** Creación de documentos embebidos, validación de respuestas dobles (409) y controles de propiedad de artículo.

## Limitaciones conocidas

* Al ejecutar la versión manual (sin Docker), la persistencia depende de JSONs efímeros en memoria y los IDs pueden solaparse.

* Las imágenes de productos se almacenan actualmente en base64 en lugar de utilizar un bucket S3 o servidor estático especializado.

* La identidad real del usuario no es comprobada externamente, y los pagos son transacciones simuladas por requerimientos académicos.

## Uso de Inteligencia Artificial

Durante el desarrollo del proyecto el equipo utilizó herramientas de inteligencia artificial asegurando transparencia, comprensión y validación posterior de las respuestas generadas:

| Herramienta | Apoyo recibido | Prompts utilizados (Ejemplos) / Validación | 
| ----- | ----- | ----- | 
| **Claude** | Programación, documentación y revisión de código en FastAPI | *"Actúa como desarrollador FastAPI. Necesito un modelo Pydantic para validar un formulario de creación de productos que valide largos de strings."* -> Se verificó e integró la clase validada. | 
| **Gemini** | Resolución de problemas, Docker Compose y PostgreSQL | *"Tengo un error de conexión entre FastAPI y el contenedor postgres en docker-compose, ¿cuál es la string de conexión correcta usando el nombre del servicio?"* -> Se ajustó el valor de `DATABASE_URL` logrando conexión exitosa. | 

El equipo comprendió, revisó, probó y adaptó manualmente los resultados generados, siendo responsable del código final del proyecto.

## Cuentas de prueba

| Rol | Nick | Contraseña | 
| ----- | ----- | ----- | 
| Usuario | `usuario` | `usuario123` | 
| Administrador | `admin` | `admin123` | 

*(Si usas el entorno Docker, existen vendedores adicionales creados en `02_datos_prueba.sql` todos con contraseña `vendedor123`)*

## Solución de problemas

* **"Address already in use":** Cierra los procesos locales u otros contenedores Docker ocupando los puertos 5432, 27018, 8000 o 5173.

* **Base de datos vacía al entrar:** Revisa si `docker-entrypoint-initdb.d/` ejecutó correctamente los archivos SQL/JS al hacer el build.

* **Fallo al levantar Docker:** Verifica que generaste el archivo `.env` a partir del `.env.example`.

## Mejoras futuras

* Cifrar comunicaciones con certificados SSL/HTTPS.

* Implementar JWT (JSON Web Tokens) en lugar de validaciones simples de autenticación en la cabecera.

* Subida de imágenes multipart directamente hacia servicios cloud.

* Reemplazar las credenciales estáticas de bases de datos por un manejador de secretos de producción.

**INFRAGANTI MARKETPLACE** — Benjamin Farias, Benjamin Villarroel, Omar Millar y Frank Häfelin.
