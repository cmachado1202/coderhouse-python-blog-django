from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


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
