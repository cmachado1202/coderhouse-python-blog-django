# Blog Django

Blog web de Carolina Machado desarrollado con Django. El proyecto se llama `blog_project` y la aplicación principal se llama `posts`. Continúa el mismo repositorio de las preentregas 7 y 8, con herencia de templates y CSS propio.

## Instalación

```bash
git clone https://github.com/cmachado1202/coderhouse-python-blog-django.git
cd coderhouse-python-blog-django
python -m venv venv
```

Activar el entorno:

- Windows PowerShell: `venv\Scripts\Activate.ps1`
- Linux/macOS: `source venv/bin/activate`

Luego instalar dependencias y levantar el servidor:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. El idioma está configurado como español de Argentina y la zona horaria como Buenos Aires. La base SQLite local y el entorno virtual están excluidos del repositorio.

`DJANGO_SECRET_KEY` puede definirse como variable de entorno para otros entornos; la clave predeterminada se utiliza únicamente para desarrollo local.

## Páginas y organización

- `/` y `/posts/`: listado de publicaciones reales, filtradas por estado publicado y ordenadas de más reciente a más antigua.
- `/acerca/`: presentación de la autora y propósito del sitio.
- `posts/urls.py`: rutas de la app, incluidas desde `blog_project/urls.py`.
- `posts/views.py`: vistas basadas en funciones que usan `render()`.
- `posts/templates/posts/base.html`: HTML5, menú, carga de static y bloque de contenido.
- `posts/templates/posts/inicio.html` y `acerca.html`: heredan la plantilla base.
- `posts/static/posts/css/estilos.css`: estilos y adaptación a pantallas pequeñas.

## Preentrega 9: modelos, ORM y admin

`posts/models.py` define `Post` con título, contenido, autor, fecha automática y estado (borrador, publicado o archivado). `__str__` devuelve el título. La migración inicial está incluida en `posts/migrations/`.

Después de `python manage.py migrate`, creá tu propio administrador local:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Entrá a `http://127.0.0.1:8000/admin/` con ese usuario. En **Posts → Añadir**, cargá al menos tres publicaciones con distintos estados. `PostAdmin` muestra título, autor, estado y fecha, con búsqueda y filtros. Los borradores y archivados quedan fuera del listado público. La vista `lista_posts` consulta el ORM y el template `lista_posts.html` recorre `{% for post in posts %}`.

Los usuarios y la base SQLite se crean en cada equipo; no se publican contraseñas ni `db.sqlite3`.

## Comprobación

Ejecutar `python manage.py check` y `python manage.py test`. Las pruebas verifican la carga de tres posts mediante los formularios del admin y que el listado público obtiene datos del ORM sin exponer borradores. Para recorrer el sitio, iniciar `python manage.py runserver`. El CSS se sirve desde `/static/posts/css/estilos.css`.
