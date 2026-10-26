from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q

def inicio(request):
    return lista_posts(request)


def lista_posts(request):
    posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts})


def acerca(request):
    return render(request, 'posts/acerca.html')


def detalle_post(request, pk):
    permitidos = Post.objects.all()
    if not request.user.is_staff:
        filtro = Q(estado="publicado")
        if request.user.is_authenticated:
            filtro |= Q(creado_por=request.user)
        permitidos = permitidos.filter(filtro)
    post = get_object_or_404(permitidos, pk=pk)
    puede_editar = request.user.is_authenticated and (request.user.is_staff or post.creado_por_id == request.user.pk)
    return render(request, "posts/post_detail.html", {"post": post, "puede_editar": puede_editar})


@login_required
def crear_post(request):
    form = PostForm(request.POST if request.method == "POST" else None, request.FILES or None,
                    initial={"autor": request.user.get_full_name() or request.user.username})
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.creado_por = request.user
        post.save()
        return redirect("posts:detalle_post", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "titulo_pagina": "Crear publicación"})


@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_staff and post.creado_por_id != request.user.pk:
        raise PermissionDenied
    form = PostForm(request.POST if request.method == "POST" else None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("posts:detalle_post", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "titulo_pagina": "Editar publicación"})


@login_required
def borrar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_staff and post.creado_por_id != request.user.pk:
        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        return redirect("posts:lista_posts")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


@login_required
def mis_posts(request):
    posts = Post.objects.filter(creado_por=request.user).order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts, "mis_publicaciones": True})
