def obtenerUsuario(correo):
    try:
        from .models import Usuario
        return Usuario.objects.get(correo=correo)
    except Exception:
        return None