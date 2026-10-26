from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from .forms import PerfilForm, RegistroForm
from .models import Perfil


@transaction.atomic
def registro(request):
    form = RegistroForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        # La señal cubre también usuarios creados desde el admin.
        Perfil.objects.get_or_create(user=usuario)
        return redirect("accounts:login")
    return render(request, "accounts/form.html", {"form": form, "titulo_pagina": "Crear una cuenta", "accion": "Registrarme"})


@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, "accounts/perfil.html", {"perfil": perfil_usuario})


@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)
    form = PerfilForm(request.POST if request.method == "POST" else None, request.FILES or None, instance=perfil_usuario)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("accounts:perfil")
    return render(request, "accounts/form.html", {"form": form, "titulo_pagina": "Editar mi perfil", "accion": "Guardar perfil"})
