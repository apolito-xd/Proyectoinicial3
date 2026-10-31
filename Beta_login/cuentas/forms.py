from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class FormularioIngreso(AuthenticationForm):
    """inicio de secion en django"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password"].label = "Contraseña"
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"


class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email


class FormularioPerfil(forms.ModelForm):
    """se editan los datos de usuario"""

    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Nombre", "last_name": "Apellido"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        otros = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if otros.exists():
            raise forms.ValidationError("Ya existe otra cuenta con este correo.")
        return email
