from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("titulo", "contenido", "autor", "estado", "imagen")
        widgets = {"contenido": forms.Textarea(attrs={"rows": 10})}

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if not titulo:
            raise forms.ValidationError("Escribí un título.")
        return titulo
