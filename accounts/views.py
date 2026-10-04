from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from .forms import PerfilForm, RegistroForm
from .models import Perfil


def registro(request):
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            usuario = form.save()
            Perfil.objects.get_or_create(user=usuario)
        return redirect('accounts:login')
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'accounts/perfil.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:perfil')
    return render(request, 'accounts/perfil_form.html', {'form': form})
