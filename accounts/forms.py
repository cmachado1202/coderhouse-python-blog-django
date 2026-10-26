from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("biografia", "avatar", "link_web")
        widgets = {"biografia": forms.Textarea(attrs={"rows": 5})}
