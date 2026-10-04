from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post


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
