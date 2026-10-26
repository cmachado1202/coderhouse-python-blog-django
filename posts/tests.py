from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from io import BytesIO
from PIL import Image
from tempfile import TemporaryDirectory


class PublicacionesTests(TestCase):
    def test_listado_solo_muestra_publicados_y_escapa_html(self):
        Post.objects.create(titulo="Borrador privado", contenido="No publicar", autor="Demo")
        publicado = Post.objects.create(titulo="Visible <script>", contenido="Contenido dinámico", autor="Demo", estado="publicado")
        response = self.client.get(reverse("posts:inicio"))
        self.assertContains(response, "Visible &lt;script&gt;")
        self.assertNotContains(response, "Borrador privado")
        self.assertContains(response, publicado.contenido)

    def test_admin_permite_cargar_tres_posts(self):
        admin = get_user_model().objects.create_superuser("admin_demo", password="solo-test-no-es-una-cuenta-real")
        self.client.force_login(admin)
        for numero, estado in enumerate(("publicado", "borrador", "archivado"), 1):
            response = self.client.post(reverse("admin:posts_post_add"), {
                "titulo": f"Prueba desde el admin {numero}", "contenido": "Contenido de prueba",
                "autor": "Demo", "estado": estado, "_save": "Guardar",
            })
            self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(str(Post.objects.first()), "Prueba desde el admin 3")


def imagen_prueba(nombre="imagen.png"):
    buffer = BytesIO()
    Image.new("RGB", (16, 16), "green").save(buffer, "PNG")
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/png")


class CrudTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user("autora", password="solo-test")
        self.client.force_login(self.usuario)

    def test_crear_editar_imagen_detalle_y_borrar_con_confirmacion(self):
        with TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            datos = {"titulo": "Post con imagen", "contenido": "Texto completo", "autor": "Demo", "estado": "publicado"}
            response = self.client.post(reverse("posts:crear_post"), {**datos, "imagen": imagen_prueba()})
            post = Post.objects.get()
            self.assertRedirects(response, reverse("posts:detalle_post", args=[post.pk]))
            self.assertTrue(post.imagen.storage.exists(post.imagen.name))
            self.assertContains(self.client.get(response.url), post.imagen.url)
            response = self.client.post(reverse("posts:editar_post", args=[post.pk]), {**datos, "titulo": "Título editado", "imagen": imagen_prueba("otra.png")})
            post.refresh_from_db()
            self.assertEqual(post.titulo, "Título editado")
            self.assertIn("otra", post.imagen.name)
            borrar_url = reverse("posts:borrar_post", args=[post.pk])
            self.assertContains(self.client.get(borrar_url), "Sí, eliminar")
            self.assertTrue(Post.objects.filter(pk=post.pk).exists())
            self.assertRedirects(self.client.post(borrar_url), reverse("posts:lista_posts"))
            self.assertFalse(Post.objects.exists())

    def test_imagen_opcional_y_archivo_invalido_rechazado(self):
        datos = {"titulo": "Sin imagen", "contenido": "Texto", "autor": "Demo", "estado": "publicado"}
        self.client.post(reverse("posts:crear_post"), datos)
        post = Post.objects.get()
        self.assertFalse(post.imagen)
        self.assertEqual(self.client.get(reverse("posts:detalle_post", args=[post.pk])).status_code, 200)
        response = self.client.post(reverse("posts:crear_post"), {**datos, "imagen": SimpleUploadedFile("malo.png", b"no es una imagen", content_type="image/png")})
        self.assertEqual(response.status_code, 200)
        self.assertIn("imagen", response.context["form"].errors)
        self.assertEqual(Post.objects.count(), 1)
