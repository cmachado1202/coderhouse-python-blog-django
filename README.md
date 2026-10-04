# Blog de Carolina · Django

Blog web desarrollado durante el curso de Python de Coderhouse. Continúa el proyecto inicial `blog_project` y la app `posts`: páginas con templates y CSS, publicaciones persistentes, CRUD con imágenes y usuarios con perfiles.

**Autora:** Carolina Machado.

## Tecnologías

Python 3.12, Django 5.2.6, SQLite, Pillow, HTML5 y CSS. Las versiones instaladas están en `requirements.txt`.

## Instalación

```bash
git clone https://github.com/cmachado1202/coderhouse-python-blog-django.git
cd coderhouse-python-blog-django
python -m venv venv
```

Activar el entorno:

- Windows PowerShell: `venv\Scripts\Activate.ps1`
- Linux/macOS: `source venv/bin/activate`

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. El superusuario es opcional para recorrer el sitio y necesario para administrar desde `/admin/`; definir su contraseña localmente.

Idioma: español de Argentina. Zona horaria: Buenos Aires. `DJANGO_SECRET_KEY` puede definirse en el entorno del proceso; `.env.example` documenta el nombre, sin claves reales. El proyecto no carga automáticamente un archivo `.env`. La clave predeterminada es solo para desarrollo local. `DEBUG=True` y las rutas media están preparados para desarrollo.

## Funcionalidades y rutas

| Ruta | Función | Acceso |
| --- | --- | --- |
| `/` y `/posts/` | Lista de posts publicados, del más nuevo al más antiguo | Público |
| `/acerca/` | Autora y propósito del blog | Público |
| `/post/<id>/` | Detalle, contenido e imagen opcional | Público para publicados |
| `/post/nuevo/` | Crear un post | Sesión iniciada |
| `/post/<id>/editar/` | Editar texto, estado e imagen | Sesión iniciada |
| `/post/<id>/eliminar/` | Confirmar y borrar mediante POST | Sesión iniciada |
| `/accounts/registro/` | Crear una cuenta con validación de contraseña | Público |
| `/accounts/login/` | Iniciar sesión | Público |
| `/accounts/logout/` | Cerrar sesión mediante POST | Desde el menú |
| `/accounts/perfil/` | Ver el perfil propio | Sesión iniciada |
| `/accounts/perfil/editar/` | Editar biografía y avatar propios | Sesión iniciada |
| `/admin/` | Administración de posts, usuarios y perfiles | Administrador |

Las vistas de escritura usan `@login_required`. El menú cambia según la sesión. Los visitantes anónimos no pueden ver borradores o archivados por URL directa. En esta versión académica, cualquier usuario autenticado puede gestionar posts; la edición de perfiles siempre se limita al usuario actual.

## Modelos y templates

`Post` incluye `titulo`, `contenido`, `autor`, `fecha_creacion` automática, `estado` y `imagen` opcional. `PostAdmin` muestra título, autor, estado y fecha, con filtros y búsqueda.

`Perfil` se vincula con `User` mediante `OneToOneField` y contiene biografía y avatar opcional. Se crea al registrar un usuario; una señal `post_save` cubre también usuarios creados por el admin y `get_or_create()` evita duplicados. `Profile` es un alias de la misma clase para la nomenclatura del checklist.

Las páginas heredan `posts/base.html`, usan rutas con nombres y cargan el CSS mediante `{% load static %}`. Los formularios de posts y perfil usan `enctype="multipart/form-data"` y procesan `request.FILES`.

## Reconstruir y probar desde cero

La base `db.sqlite3`, `media/`, el entorno virtual y archivos privados no se suben. Las migraciones incluidas reconstruyen todas las tablas. Para cargar datos:

1. Ejecutar los comandos de instalación y crear un superusuario.
2. Entrar a `/admin/`, sección Posts, y agregar tres publicaciones: una publicada, una borrador y una archivada.
3. Abrir inicio: solo se muestra la publicada. El admin permite cambiar su estado.
4. Registrarse desde el sitio e iniciar sesión. Crear un post con una imagen PNG/JPEG y estado publicado, abrir su detalle y editar para reemplazar la imagen.
5. Crear un post sin imagen: listado y detalle deben funcionar igualmente.
6. Abrir “Mi perfil”, editar la biografía y subir un avatar. Confirmar que se muestra en el perfil.
7. Abrir “Eliminar” en un post: primero se muestra confirmación. Solo “Confirmar eliminación” borra el registro.
8. Cerrar sesión desde el menú. Intentar `/post/nuevo/` o editar un post: se redirige al login.

Las imágenes nuevas se almacenan en `media/posts/` y `media/avatares/`. `MEDIA_ROOT` usa `BASE_DIR` y `MEDIA_URL='/media/'`; Django las sirve cuando `DEBUG=True`. Para probar nuevamente las imágenes en una instalación limpia hay que volver a subirlas.

## Verificación

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Las pruebas usan una base temporal y archivos de imagen temporales: listado y estados, carga desde admin, CRUD con y sin imágenes, confirmación de borrado, registro/login/logout, perfil y protección de rutas. Con `runserver`, verificar en el navegador que `/static/posts/css/estilos.css` responde HTTP 200 y que el menú y las imágenes cargan.

## Etapas del repositorio

`main` conserva la preentrega 8 enviada. Las ramas `preentrega-9`, `preentrega-10` y `preentrega-11` preparan los siguientes checkpoints. La rama `proyecto-final` consolida el trabajo completo; las entregas se enviarán cuando Coderhouse las habilite.
