# Blog Django

Base inicial de un blog web con Django. El proyecto se llama `blog_project` y la aplicación principal se llama `posts`. Esta etapa prepara la configuración; las publicaciones web se desarrollarán en módulos posteriores.

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
