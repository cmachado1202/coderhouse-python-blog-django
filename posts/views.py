from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import PostForm

def inicio(request):
    return lista_posts(request)


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')
    return render(request, 'posts/lista_posts.html', {'posts': posts})


def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


def crear_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save()
        return redirect('posts:detalle_post', pk=post.pk)
    return render(request, 'posts/post_form.html', {'form': form, 'titulo_pagina': 'Crear publicación'})


def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('posts:detalle_post', pk=post.pk)
    return render(request, 'posts/post_form.html', {'form': form, 'titulo_pagina': 'Editar publicación'})


def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:lista_posts')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})
