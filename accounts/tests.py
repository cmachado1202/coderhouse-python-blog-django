from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Perfil
from posts.models import Post
from PIL import Image
from io import BytesIO
import tempfile


class UsuariosTests(TestCase):
    def test_registro_login_logout_y_perfil(self):
        data = {'username': 'nueva_autora', 'email': 'prueba@example.com', 'password1': 'Prueba-larga-2026!', 'password2': 'Prueba-larga-2026!'}
        response = self.client.post(reverse('accounts:registro'), data)
        self.assertRedirects(response, reverse('accounts:login'))
        usuario = get_user_model().objects.get(username='nueva_autora')
        self.assertEqual(Perfil.objects.filter(user=usuario).count(), 1)
        response = self.client.post(reverse('accounts:login'), {'username': data['username'], 'password': data['password1']})
        self.assertRedirects(response, reverse('posts:lista_posts'))
        self.assertContains(self.client.get(reverse('accounts:perfil')), 'nueva_autora')
        self.assertContains(self.client.get(reverse('posts:inicio')), 'Cerrar sesión')
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('posts:lista_posts'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(self.client.get(reverse('posts:inicio')), 'Iniciar sesión')

    def test_rutas_protegidas_y_publicaciones_privadas(self):
        post = Post.objects.create(titulo='Publicado', contenido='Texto', autor='Carolina', estado='publicado')
        privado = Post.objects.create(titulo='Borrador', contenido='Texto privado', autor='Carolina')
        for url in [reverse('posts:crear_post'), reverse('posts:editar_post', args=[post.pk]), reverse('posts:eliminar_post', args=[post.pk]), reverse('accounts:perfil'), reverse('accounts:editar_perfil')]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('accounts:login')))
        self.assertEqual(self.client.get(reverse('posts:detalle_post', args=[post.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('posts:detalle_post', args=[privado.pk])).status_code, 404)

    def test_avatar_y_biografia_solo_modifican_perfil_propio(self):
        usuario = get_user_model().objects.create_user(username='uno', password='clave-temporal-prueba')
        otro = get_user_model().objects.create_user(username='dos')
        self.client.force_login(usuario)
        buffer = BytesIO()
        Image.new('RGB', (4, 4), 'blue').save(buffer, 'PNG')
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            response = self.client.post(reverse('accounts:editar_perfil'), {'biografia': 'Aprendiendo Django', 'avatar': SimpleUploadedFile('avatar.png', buffer.getvalue(), content_type='image/png')})
            self.assertRedirects(response, reverse('accounts:perfil'))
            usuario.perfil.refresh_from_db()
            self.assertEqual(usuario.perfil.biografia, 'Aprendiendo Django')
            self.assertTrue(usuario.perfil.avatar)
            self.assertContains(self.client.get(reverse('accounts:perfil')), usuario.perfil.avatar.url)
            self.assertEqual(otro.perfil.biografia, '')

    def test_registro_invalido_no_crea_usuario(self):
        response = self.client.post(reverse('accounts:registro'), {'username': 'error', 'password1': 'a', 'password2': 'b'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(get_user_model().objects.filter(username='error').exists())
