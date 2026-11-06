import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


def dominio_recibe_correo(dominio):
    """True si el dominio tiene servidor de correo (registro MX)."""
    try:
        respuesta = dns.resolver.resolve(dominio, "MX", lifetime=5)
        return any(str(r.exchange) != "." for r in respuesta)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False
    except dns.exception.DNSException:
        # sin internet o DNS caído: no bloqueamos al usuario por un problema nuestro
        return True


class FormularioIngreso(AuthenticationForm):
    """inicio de secion en django"""

    error_messages = {
        **AuthenticationForm.error_messages,
        "inactive": "Tu cuenta aún no está activada. Abre el enlace que enviamos a tu correo.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password"].label = "Contraseña"
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"

    def clean(self):
        # Django trata igual a una cuenta sin activar y a una clave mala.
        # Aquí se avisa claramente cuando la clave es correcta pero falta confirmar el correo.
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            usuario = User.objects.filter(username=username).first()
            if usuario and not usuario.is_active and usuario.check_password(password):
                raise forms.ValidationError(self.error_messages["inactive"], code="inactive")
        return super().clean()


class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if not dominio_recibe_correo(email.split("@")[-1]):
            raise forms.ValidationError(
                "Ese dominio no recibe correos. Revisa que la dirección esté bien escrita."
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email


class FormularioPerfil(forms.ModelForm):
    """se editan los datos de usuario"""

    class Meta:
        model = User
        fields = ("first_name", "last_name")
        labels = {"first_name": "Nombre", "last_name": "Apellido"}
