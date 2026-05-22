from django.core.mail import send_mail
from django.conf import settings


# ──────────────────────────────────────────────
# Helpers de usuario
# ──────────────────────────────────────────────

def obtenerUsuario(correo):
    """Devuelve el objeto Usuario o None."""
    try:
        from .models import Usuario
        return Usuario.objects.get(correo=correo)
    except Exception:
        return None


# ──────────────────────────────────────────────
# Correo de verificación
# ──────────────────────────────────────────────

def enviar_codigo_verificacion(usuario):
    """
    Genera un código nuevo, lo guarda en el usuario y envía el correo.
    Retorna True si el envío fue exitoso, False si falló.
    """
    codigo = usuario.generar_nuevo_codigo()

    asunto = 'Verifica tu cuenta — Sistema de Tareas'
    cuerpo = (
        f'Hola {usuario.nombre},\n\n'
        f'Tu código de verificación es:\n\n'
        f'    {codigo}\n\n'
        f'Ingresa este código en la página de verificación para activar tu cuenta.\n'
        f'El código expira cuando generes uno nuevo.\n\n'
        f'Si no creaste esta cuenta, ignora este mensaje.\n\n'
        f'— Sistema de Tareas'
    )

    try:
        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.correo],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'[ERROR email] {e}')
        return False


# ──────────────────────────────────────────────
# Helpers de sesión
# ──────────────────────────────────────────────

def guardar_sesion(request, usuario):
    """Guarda los datos del usuario en la sesión."""
    request.session['correo'] = usuario.correo
    request.session['nombre'] = usuario.nombre
    request.session['rol'] = usuario.rol
    request.session['foto_perfil'] = usuario.foto_perfil or ''


def limpiar_sesion(request):
    """Elimina todos los datos de sesión."""
    request.session.flush()


def usuario_en_sesion(request):
    """Devuelve True si hay un usuario logueado."""
    return bool(request.session.get('correo'))


def rol_en_sesion(request):
    """Devuelve el rol del usuario logueado o ''."""
    return request.session.get('rol', '')