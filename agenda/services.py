def obtenerTareasPorUsuario(correo):
    try:
        from tareas.services import obtenerTareasPorUsuario as getTareas
        return getTareas(correo)
    except Exception:
        return []


def obtenerTarea(tareaId):
    try:
        from tareas.services import obtenerTarea as getTarea
        return getTarea(tareaId)
    except Exception:
        return None


def obtenerUsuario(correo):
    try:
        from usuarios.services import obtenerUsuario as getUsuario
        return getUsuario(correo)
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