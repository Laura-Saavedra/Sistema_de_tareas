def obtenerTareasPorUsuario(correo):
    try:
        from tareas.models import Tarea
        return list(Tarea.objects.filter(usuarioCorreo=correo))
    except Exception:
        return []


def obtenerTarea(tareaId):
    try:
        from tareas.models import Tarea
        return Tarea.objects.get(id=tareaId)
    except Exception:
        return None


def obtenerUsuario(correo):
    try:
        from usuarios.models import Usuario
        return Usuario.objects.get(correo=correo)
    except Exception:
        return None


def obtenerAgendasPorUsuario(correo):
    try:
        from .models import Agenda
        return list(Agenda.objects.filter(usuarioCorreo=correo))
    except Exception:
        return []


def obtenerAgendasPorEstado(estado):
    try:
        from .models import Agenda
        return list(Agenda.objects.filter(estado=estado))
    except Exception:
        return []