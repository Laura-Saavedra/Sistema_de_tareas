def obtenerUsuarioPorCedula(cedula):
    try:
        from .models import Usuario
        return Usuario.objects.get(cedula=cedula)
    except Exception:
        return None