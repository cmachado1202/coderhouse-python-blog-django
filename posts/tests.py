from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from io import BytesIO
import tempfile


class PublicacionesTests(TestCase):
    def test_inicio_solo_muestra_publicados_en_orden_reciente(self):
        Post.objects.create(titulo='Borrador privado', contenido='No publicar', autor='Carolina')
        viejo = Post.objects.create(titulo='Primer artículo', contenido='Python', autor='Carolina', estado='publicado')
        nuevo = Post.objects.create(titulo='Segundo artículo', contenido='Django', autor='Carolina', estado='publicado')
        response = self.client.get(reverse('posts:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['posts']), [nuevo, viejo])
        self.assertNotContains(response, 'Borrador privado')
        self.assertContains(response, 'Primer artículo')

    def test_admin_permite_cargar_posts(self):
        admin = get_user_model().objects.create_superuser(username='admin_prueba', password='clave-temporal-prueba')
        self.client.force_login(admin)
        for i, estado in enumerate(['publicado', 'borrador', 'archivado']):
            response = self.client.post(reverse('admin:posts_post_add'), {'titulo': f'Artículo {i}', 'contenido': 'Texto de prueba', 'autor': 'Carolina', 'estado': estado, '_save': 'Guardar'})
            self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 3)
        response = self.client.get(reverse('admin:posts_post_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Artículo 0')

    def test_listado_vacio_y_acerca(self):
        self.assertContains(self.client.get(reverse('posts:inicio')), 'Todavía no hay publicaciones')
        self.assertContains(self.client.get(reverse('posts:acerca')), 'Carolina Machado')


class CrudTests(TestCase):
    def setUp(self):
        usuario = get_user_model().objects.create_user(username='autor_prueba', password='clave-temporal-prueba')
        self.client.force_login(usuario)
        self.media = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(self.media.cleanup)

    def imagen(self, nombre='prueba.png'):
        buffer = BytesIO()
        Image.new('RGB', (4, 4), 'green').save(buffer, format='PNG')
        return SimpleUploadedFile(nombre, buffer.getvalue(), content_type='image/png')

    def test_crear_editar_imagen_y_borrar_con_confirmacion(self):
        data = {'titulo': 'Post con imagen', 'contenido': 'Contenido', 'autor': 'Carolina', 'estado': 'publicado', 'imagen': self.imagen()}
        response = self.client.post(reverse('posts:crear_post'), data)
        post = Post.objects.get()
        self.assertRedirects(response, reverse('posts:detalle_post', args=[post.pk]))
        self.assertContains(self.client.get(response.url), post.imagen.url)
        anterior = post.imagen.name
        data['titulo'] = 'Post editado'
        data['imagen'] = self.imagen('otra.png')
        self.client.post(reverse('posts:editar_post', args=[post.pk]), data)
        post.refresh_from_db()
        self.assertEqual(post.titulo, 'Post editado')
        self.assertNotEqual(post.imagen.name, anterior)
        url = reverse('posts:eliminar_post', args=[post.pk])
        self.assertContains(self.client.get(url), 'Confirmar eliminación')
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('posts:lista_posts'))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_sin_imagen_y_formulario_invalido(self):
        data = {'titulo': 'Sin imagen', 'contenido': 'Texto', 'autor': 'Carolina', 'estado': 'publicado'}
        self.client.post(reverse('posts:crear_post'), data)
        post = Post.objects.get()
        self.assertFalse(post.imagen)
        self.assertEqual(self.client.get(reverse('posts:detalle_post', args=[post.pk])).status_code, 200)
        response = self.client.post(reverse('posts:crear_post'), {'titulo': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Post.objects.count(), 1)
