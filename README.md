# Blog Django

Blog web de Carolina Machado desarrollado con Django. El proyecto se llama `blog_project` y la aplicación principal se llama `posts`. La preentrega 8 continúa la base aprobada en la preentrega 7: suma páginas de inicio y acerca de, templates con herencia y CSS propio.

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

- `/`: bienvenida y descripción del blog.
- `/acerca/`: presentación de la autora y propósito del sitio.
- `posts/urls.py`: rutas de la app, incluidas desde `blog_project/urls.py`.
- `posts/views.py`: vistas basadas en funciones que usan `render()`.
- `posts/templates/posts/base.html`: HTML5, menú, carga de static y bloque de contenido.
- `posts/templates/posts/inicio.html` y `acerca.html`: heredan la plantilla base.
- `posts/static/posts/css/estilos.css`: estilos y adaptación a pantallas pequeñas.

Esta etapa usa contenido estático; todavía no incorpora modelos ni formularios de publicaciones.

## Comprobación

Ejecutar `python manage.py check`, iniciar `python manage.py runserver` y recorrer ambas páginas desde el menú. En las herramientas del navegador, verificar que `/static/posts/css/estilos.css` responda con HTTP 200. Las rutas y el CSS deben funcionar en una instalación nueva siguiendo los pasos anteriores.
