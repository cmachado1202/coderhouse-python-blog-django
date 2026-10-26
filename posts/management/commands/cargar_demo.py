from django.core.management.base import BaseCommand
from posts.models import Post


class Command(BaseCommand):
    help = "Carga tres publicaciones ficticias para explorar el blog (sin crear usuarios)."

    def handle(self, *args, **options):
        ejemplos = [
            ("Mi primer modelo en Django", "Un modelo describe los campos que se guardan en la base de datos. Las migraciones sincronizan ese diseño con SQLite.", "publicado"),
            ("Del formulario a la publicación", "ModelForm valida los datos y permite crear publicaciones con una imagen opcional. El servidor decide cuándo guardar los cambios.", "publicado"),
            ("Próximas notas del proyecto", "Este borrador sirve para comprobar que el contenido pendiente no aparece en el listado público.", "borrador"),
        ]
        for titulo, contenido, estado in ejemplos:
            _, creado = Post.objects.get_or_create(titulo=titulo, defaults={"contenido": contenido, "autor": "Demo educativa", "estado": estado})
            self.stdout.write(f"{'Creado' if creado else 'Ya existe'}: {titulo}")
