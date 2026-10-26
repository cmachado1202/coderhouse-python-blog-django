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

## Preentrega 10: CRUD e imágenes

El menú del listado permite crear publicaciones; cada título abre su detalle, con enlaces para editar o eliminar. El borrado muestra una confirmación y solo elimina mediante POST con CSRF. `PostForm` es un `ModelForm` con título, contenido, autor, estado e imagen opcional.

`ImageField(upload_to='posts/', null=True, blank=True)` guarda las imágenes bajo `media/posts/`. Pillow valida los archivos; el formulario usa `enctype="multipart/form-data"` y las vistas reciben `request.FILES`. `MEDIA_URL='/media/'` y `MEDIA_ROOT` están configurados y las rutas sirven archivos solo en desarrollo (`DEBUG`). Los archivos media locales no se suben a GitHub.

Para probar: crear un post con imagen, abrir su detalle, editar el título y reemplazar la imagen, y eliminarlo con confirmación. Repetir sin imagen para comprobar que es opcional.

## Preentrega 11: usuarios y perfiles

`accounts` agrega registro (`UserCreationForm` personalizado), login y logout nativos de Django. El logout usa **POST con CSRF**, nunca un enlace GET. `Perfil` tiene `OneToOneField` con el usuario, biografía, avatar opcional y enlace web. Una señal `post_save` crea perfiles también para usuarios del admin; el registro y las vistas usan `get_or_create` sin duplicar perfiles.

- `/accounts/registro/`: crear una cuenta local; después, iniciar sesión.
- `/accounts/login/`: ingresar. Si venías de una ruta protegida, vuelve a esa ruta.
- `/accounts/perfil/` y `/accounts/perfil/editar/`: ver y editar solo el propio perfil.
- `/post/nuevo/`, `/post/<id>/editar/`, `/post/<id>/borrar/`: requieren autenticación. Editar y borrar requieren además ser propietario o staff.
- `/mis-posts/`: permite al autor volver a sus borradores y archivados.
- Listado y detalle de publicaciones publicadas: públicos. El contenido de borradores queda disponible únicamente para su propietario o staff.

Los posts del admin pueden gestionarse por staff. `creado_por` permite relacionar cada nuevo post con su propietario sin perder el campo de autor de los checkpoints previos. Los perfiles de usuarios anteriores se crean al abrir su perfil. Los avatares usan `media/avatares/` con la configuración de media y Pillow del checkpoint 10.

Aplicá `python manage.py migrate` después de actualizar el repositorio. Para probar usuarios: registrar una cuenta, iniciar sesión, editar la biografía, cargar un avatar, crear un post, cerrar sesión e intentar entrar directamente a `/post/nuevo/`; debe redirigir al login. No se incluye ninguna cuenta o contraseña real en el repositorio.

## Comprobación final

`python manage.py cargar_demo` carga tres notas educativas ficticias (dos publicadas y un borrador) para explorar el proyecto. Es opcional y se puede repetir sin duplicarlas. No reemplaza el ejercicio de cargar posts desde el admin. La prueba de integración del admin verifica además la creación de tres posts usando sus formularios.

Ejecutar `python manage.py check` y `python manage.py test`. Las pruebas verifican la carga de tres posts mediante los formularios del admin y que el listado público obtiene datos del ORM sin exponer borradores. Para recorrer el sitio, iniciar `python manage.py runserver`. El CSS se sirve desde `/static/posts/css/estilos.css`.

La verificación del 26/10/2026 se repitió instalando únicamente `requirements.txt` en un entorno virtual nuevo: **7 pruebas aprobadas**. También se aplicaron migraciones en una SQLite aislada, se creó un superusuario local y se cargaron tres posts (publicado, borrador y archivado) mediante las vistas reales de `/admin/`; el listado público mostró únicamente el publicado. El resumen reproducible de esa ejecución está en `evidencias/validacion_preentregas_26-10-2026.json`, sin credenciales ni base de datos. Es evidencia de una comprobación automatizada, no una captura de una navegación manual.
