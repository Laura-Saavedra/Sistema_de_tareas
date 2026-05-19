def obtenerTarea(tareaId):
    try:
        from .models import Tarea
        return Tarea.objects.get(id=tareaId)
    except Exception:
        return None


def obtenerTareasPorUsuario(correo):
    try:
        from .models import Tarea
        return list(Tarea.objects.filter(usuarioCorreo=correo))
    except Exception:
        return []