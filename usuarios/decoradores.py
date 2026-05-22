from functools import wraps
from django.shortcuts import redirect


def login_requerido(view_func):
    """
    Redirige al login si no hay sesión activa.
    Uso: @login_requerido
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('correo'):
            return redirect('Login')
        return view_func(request, *args, **kwargs)
    return wrapper


def rol_requerido(*roles):
    """
    Permite el acceso solo a los roles indicados.
    Redirige al dashboard si el rol no coincide.
    Uso: @rol_requerido('profesor')  o  @rol_requerido('profesor', 'estudiante')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('correo'):
                return redirect('Login')
            if request.session.get('rol') not in roles:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# ──────────────────────────────────────────────
# Mixin equivalente para vistas basadas en clase
# ──────────────────────────────────────────────

class LoginRequeridoMixin:
    """
    Mixin para class-based views. Equivale a @login_requerido.
    Uso: class MiVista(LoginRequeridoMixin, ListView): ...
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('correo'):
            return redirect('Login')
        return super().dispatch(request, *args, **kwargs)


class RolRequeridoMixin:
    """
    Mixin para class-based views con control de rol.
    Define roles_permitidos = ['profesor'] en la vista.
    """
    roles_permitidos = []

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('correo'):
            return redirect('Login')
        if request.session.get('rol') not in self.roles_permitidos:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)