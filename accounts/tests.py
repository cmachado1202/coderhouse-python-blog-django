from tempfile import TemporaryDirectory
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Perfil
from posts.models import Post
from posts.tests import imagen_prueba


class UsuariosTests(TestCase):
    def test_registro_login_perfil_avatar_logout(self):
        with TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            datos = {"username": "lectora", "email": "demo@example.com", "password1": "Prueba-Local-2026-Segura", "password2": "Prueba-Local-2026-Segura"}
            response = self.client.post(reverse("accounts:registro"), datos)
            self.assertRedirects(response, reverse("accounts:login"))
            usuario = get_user_model().objects.get(username="lectora")
            self.assertEqual(Perfil.objects.filter(user=usuario).count(), 1)
            response = self.client.post(reverse("accounts:login"), {"username": "lectora", "password": datos["password1"]})
            self.assertRedirects(response, reverse("posts:lista_posts"))
            self.assertContains(self.client.get(reverse("accounts:perfil")), "demo@example.com")
            response = self.client.post(reverse("accounts:editar_perfil"), {"biografia": "Aprendiendo Django", "avatar": imagen_prueba("avatar.png"), "link_web": "https://example.com"})
            self.assertRedirects(response, reverse("accounts:perfil"))
            usuario.perfil.refresh_from_db()
            self.assertEqual(usuario.perfil.biografia, "Aprendiendo Django")
            self.assertContains(self.client.get(response.url), usuario.perfil.avatar.url)
            self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
            self.assertRedirects(self.client.post(reverse("accounts:logout")), reverse("posts:lista_posts"))
            self.assertRedirects(self.client.get(reverse("accounts:perfil")), reverse("accounts:login") + "?next=" + reverse("accounts:perfil"))

    def test_rutas_protegidas_y_autorizacion_entre_usuarios(self):
        propietario = get_user_model().objects.create_user("propietario")
        ajeno = get_user_model().objects.create_user("ajeno")
        post = Post.objects.create(titulo="Artículo", contenido="Contenido", autor="Autor", estado="publicado", creado_por=propietario)
        rutas = [reverse("posts:crear_post"), reverse("posts:editar_post", args=[post.pk]), reverse("posts:borrar_post", args=[post.pk])]
        for url in rutas:
            self.assertEqual(self.client.get(url).status_code, 302)
            self.assertEqual(self.client.post(url, {}).status_code, 302)
        self.client.force_login(ajeno)
        for url in rutas[1:]:
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url, {}).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        post.estado = "borrador"
        post.save()
        self.assertEqual(self.client.get(reverse("posts:detalle_post", args=[post.pk])).status_code, 404)
        self.client.force_login(propietario)
        self.assertEqual(self.client.get(reverse("posts:detalle_post", args=[post.pk])).status_code, 200)
        self.assertContains(self.client.get(reverse("posts:mis_posts")), post.titulo)

    def test_registro_invalido_no_crea_usuario_ni_perfil(self):
        response = self.client.post(reverse("accounts:registro"), {"username": "nuevo", "password1": "a", "password2": "b"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.exists())
        self.assertFalse(Perfil.objects.exists())
