from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('post/nuevo/', views.crear_post, name='crear_post'),
    path('post/<int:pk>/', views.detalle_post, name='detalle_post'),
    path('post/<int:pk>/editar/', views.editar_post, name='editar_post'),
    path('post/<int:pk>/borrar/', views.borrar_post, name='borrar_post'),
    path('acerca/', views.acerca, name='acerca'),
]
