import os
import uuid

from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario
from .services import (
    enviar_codigo_verificacion,
    guardar_sesion,
    limpiar_sesion,
    obtenerUsuario,
)
from .decoradores import login_requerido


# ──────────────────────────────────────────────
# REGISTRO
# ──────────────────────────────────────────────

def registroUsuario(request):
    """Crea el usuario (sin verificar) y envía el código al correo."""
    if request.session.get('correo'):
        return redirect('dashboard')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip().lower()
        password = request.POST.get('password', '')
        confirmar = request.POST.get('confirmar_password', '')
        rol = request.POST.get('rol', 'estudiante')

        # ── Validaciones ──
        errores = []

        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not apellido:
            errores.append('El apellido es obligatorio.')
        if not correo:
            errores.append('El correo es obligatorio.')
        if not password:
            errores.append('La contraseña es obligatoria.')
        if password != confirmar:
            errores.append('Las contraseñas no coinciden.')
        if len(password) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres.')
        if rol not in ('profesor', 'estudiante'):
            errores.append('Rol inválido.')

        if not errores and Usuario.objects.filter(correo=correo).exists():
            errores.append('Ya existe una cuenta con ese correo.')

        if errores:
            return render(request, 'usuarios/registro.html', {
                'errores': errores,
                'datos': request.POST,
            })

        # ── Crear usuario sin verificar ──
        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            password=make_password(password),
            rol=rol,
            verificado=False,
        )

        # ── Enviar código ──
        enviado = enviar_codigo_verificacion(usuario)

        # Guardar correo pendiente de verificación en sesión temporal
        request.session['correo_pendiente'] = correo

        if not enviado:
            # En desarrollo se muestra el código en pantalla como fallback
            request.session['codigo_dev'] = usuario.codigo_verificacion

        return redirect('verificar_correo')

    return render(request, 'usuarios/registro.html')


# ──────────────────────────────────────────────
# VERIFICACIÓN DE CORREO
# ──────────────────────────────────────────────

def verificarCorreo(request):
    """El usuario ingresa el código de 6 dígitos recibido por email."""
    correo = request.session.get('correo_pendiente')
    if not correo:
        return redirect('Login')

    codigo_dev = request.session.get('codigo_dev', '')  # solo en desarrollo

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return redirect('Login')

        if usuario.codigo_verificacion == codigo_ingresado:
            usuario.verificado = True
            usuario.codigo_verificacion = ''
            usuario.save()

            # Limpiar sesión temporal
            request.session.pop('correo_pendiente', None)
            request.session.pop('codigo_dev', None)

            request.session['mensaje'] = '¡Cuenta verificada! Ya puedes iniciar sesión.'
            return redirect('Login')
        else:
            return render(request, 'usuarios/verificar_correo.html', {
                'error': 'Código incorrecto. Inténtalo de nuevo.',
                'correo': correo,
                'codigo_dev': codigo_dev,
            })

    return render(request, 'usuarios/verificar_correo.html', {
        'correo': correo,
        'codigo_dev': codigo_dev,
    })


def reenviarCodigo(request):
    """Reenvía un nuevo código de verificación."""
    correo = request.session.get('correo_pendiente')
    if not correo:
        return redirect('Login')

    try:
        usuario = Usuario.objects.get(correo=correo)
        enviado = enviar_codigo_verificacion(usuario)
        if not enviado:
            request.session['codigo_dev'] = usuario.codigo_verificacion
    except Usuario.DoesNotExist:
        pass

    return redirect('verificar_correo')


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────

def loginUsuario(request):
    if request.session.get('correo'):
        return redirect('dashboard')

    mensaje = request.session.pop('mensaje', None)

    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip().lower()
        password = request.POST.get('password', '')

        try:
            usuario = Usuario.objects.filter(correo=correo).first()

            if not usuario:
                return render(request, 'usuarios/login.html', {
                    'error': 'No existe una cuenta con ese correo.',
                    'correo': correo,
                })

            if not check_password(password, usuario.password):
                return render(request, 'usuarios/login.html', {
                    'error': 'Contraseña incorrecta.',
                    'correo': correo,
                })

            if not usuario.verificado:
                # Mandar a verificar
                request.session['correo_pendiente'] = correo
                return redirect('verificar_correo')

            if not usuario.activo:
                return render(request, 'usuarios/login.html', {
                    'error': 'Tu cuenta está desactivada. Contacta al administrador.',
                })

            guardar_sesion(request, usuario)
            return redirect('dashboard')

        except Exception as e:
            print(f'[ERROR login] {e}')
            return render(request, 'usuarios/login.html', {
                'error': 'Ocurrió un error al iniciar sesión.',
            })

    return render(request, 'usuarios/login.html', {'mensaje': mensaje})


# ──────────────────────────────────────────────
# LOGOUT
# ──────────────────────────────────────────────

def logoutUsuario(request):
    limpiar_sesion(request)
    return redirect('Login')


# ──────────────────────────────────────────────
# DASHBOARD DINÁMICO POR ROL
# ──────────────────────────────────────────────

@login_requerido
def dashboard(request):
    correo = request.session.get('correo')
    rol = request.session.get('rol')

    contexto = {
        'nombre': request.session.get('nombre'),
        'rol': rol,
    }

    if rol == 'profesor':
        contexto.update(_datos_dashboard_profesor(correo))
    else:
        contexto.update(_datos_dashboard_estudiante(correo))

    return render(request, 'usuarios/dashboard.html', contexto)


def _datos_dashboard_profesor(correo):
    from tareas.models import Tarea, Calificacion
    tareas_qs = Tarea.objects.filter(usuarioCorreo=correo)
    total      = tareas_qs.count()
    pendientes = tareas_qs.filter(estadoTarea='pendiente').count()
    en_proceso = tareas_qs.filter(estadoTarea='enProceso').count()
    entregadas = tareas_qs.filter(estadoTarea='entregada').count()
    completadas = tareas_qs.filter(estadoTarea='completada').count()
    recientes  = list(tareas_qs.order_by('-fechaCreacion')[:5])
    return {
        'total_tareas':       total,
        'tareas_pendientes':  pendientes,
        'tareas_en_proceso':  en_proceso,
        'tareas_entregadas':  entregadas,
        'tareas_completadas': completadas,
        'actividad_reciente': recientes,
    }


def _datos_dashboard_estudiante(correo):
    from tareas.models import Tarea, Calificacion
    from agenda.models import Agenda
    from django.utils import timezone

    tareas_qs   = Tarea.objects.filter(estudianteCorreo=correo)
    pendientes  = list(tareas_qs.filter(estadoTarea='pendiente').order_by('-fechaCreacion')[:5])
    hoy         = timezone.now().date()
    proximas    = list(
        Agenda.objects.filter(usuarioCorreo=correo, estado='pendiente', fecha__gte=hoy)
        .order_by('fecha', 'hora')[:5]
    )
    total       = tareas_qs.count()
    completadas = tareas_qs.filter(estadoTarea='completada').count()
    notas       = []
    for t in tareas_qs:
        try:
            notas.append(t.calificacion.nota)
        except Exception:
            pass
    promedio_notas = round(sum(notas) / len(notas), 2) if notas else None
    progreso       = round((completadas / total * 100), 1) if total > 0 else 0

    return {
        'tareas_pendientes_lista': pendientes,
        'proximas_entregas':       proximas,
        'promedio':                progreso,
        'promedio_notas':          promedio_notas,
        'total_tareas':            total,
        'tareas_completadas':      completadas,
    }


# ──────────────────────────────────────────────
# PERFIL
# ──────────────────────────────────────────────

@login_requerido
def perfilUsuario(request):
    correo = request.session.get('correo')
    usuario = obtenerUsuario(correo)

    if not usuario:
        limpiar_sesion(request)
        return redirect('Login')

    return render(request, 'usuarios/perfil.html', {'usuario': usuario})


# ──────────────────────────────────────────────
# EDITAR DATOS DEL PERFIL
# ──────────────────────────────────────────────

@login_requerido
def editarUsuario(request):
    correo = request.session.get('correo')
    usuario = obtenerUsuario(correo)

    if not usuario:
        limpiar_sesion(request)
        return redirect('Login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        nuevo_correo = request.POST.get('correo', '').strip().lower()

        errores = []
        if not nombre:
            errores.append('El nombre no puede estar vacío.')
        if not apellido:
            errores.append('El apellido no puede estar vacío.')
        if not nuevo_correo:
            errores.append('El correo no puede estar vacío.')

        # Si cambió el correo, verificar que no exista otro usuario con ese correo
        if nuevo_correo != correo:
            if Usuario.objects.filter(correo=nuevo_correo).exclude(correo=correo).exists():
                errores.append('Ese correo ya está en uso por otra cuenta.')

        if errores:
            return render(request, 'usuarios/editar.html', {
                'usuario': usuario,
                'errores': errores,
            })

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = nuevo_correo
        usuario.save()

        # Actualizar sesión
        request.session['nombre'] = nombre
        request.session['correo'] = nuevo_correo

        return redirect('perfilUsuario')

    return render(request, 'usuarios/editar.html', {'usuario': usuario})


# ──────────────────────────────────────────────
# CAMBIO DE CONTRASEÑA
# ──────────────────────────────────────────────

@login_requerido
def cambiarPassword(request):
    correo = request.session.get('correo')
    usuario = obtenerUsuario(correo)

    if not usuario:
        limpiar_sesion(request)
        return redirect('Login')

    if request.method == 'POST':
        actual = request.POST.get('password_actual', '')
        nueva = request.POST.get('password_nueva', '')
        confirmar = request.POST.get('confirmar_password', '')

        errores = []

        if not check_password(actual, usuario.password):
            errores.append('La contraseña actual es incorrecta.')
        if len(nueva) < 8:
            errores.append('La nueva contraseña debe tener al menos 8 caracteres.')
        if nueva != confirmar:
            errores.append('Las nuevas contraseñas no coinciden.')

        if errores:
            return render(request, 'usuarios/cambiar_password.html', {'errores': errores})

        usuario.password = make_password(nueva)
        usuario.save()

        return render(request, 'usuarios/cambiar_password.html', {
            'exito': 'Contraseña actualizada correctamente.'
        })

    return render(request, 'usuarios/cambiar_password.html')


# ──────────────────────────────────────────────
# FOTO DE PERFIL
# ──────────────────────────────────────────────

@login_requerido
def subirFotoPerfil(request):
    """Guarda la foto de perfil en MEDIA_ROOT/fotos_perfil/."""
    correo = request.session.get('correo')
    usuario = obtenerUsuario(correo)

    if not usuario:
        limpiar_sesion(request)
        return redirect('Login')

    if request.method == 'POST' and request.FILES.get('foto'):
        from django.conf import settings

        foto = request.FILES['foto']

        # Validar extensión
        ext = os.path.splitext(foto.name)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif'):
            return render(request, 'usuarios/perfil.html', {
                'usuario': usuario,
                'error_foto': 'Formato no permitido. Usa JPG, PNG, WEBP o GIF.',
            })

        # Guardar con nombre único
        nombre_archivo = f"{uuid.uuid4().hex}{ext}"
        carpeta = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil')
        os.makedirs(carpeta, exist_ok=True)
        ruta_completa = os.path.join(carpeta, nombre_archivo)

        with open(ruta_completa, 'wb+') as destino:
            for chunk in foto.chunks():
                destino.write(chunk)

        # Guardar ruta relativa en el modelo
        usuario.foto_perfil = f'fotos_perfil/{nombre_archivo}'
        usuario.save()

        request.session['foto_perfil'] = usuario.foto_perfil

    return redirect('perfilUsuario')