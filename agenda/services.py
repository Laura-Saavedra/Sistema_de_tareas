def obtenerTareasPorUsuario(cedula):
    try:
        from tareas.models import Tarea
        return list(Tarea.objects.filter(usuarioResponsableId=int(cedula)))
    except Exception:
        return []


def obtenerTarea(tareaId):
    try:
        from tareas.models import Tarea
        return Tarea.objects.get(id=tareaId)
    except Exception:
        return None


def obtenerUsuario(usuarioId):
    try:
        from usuarios.models import Usuario
        return Usuario.objects.get(id=usuarioId)
    except Exception:
        return None