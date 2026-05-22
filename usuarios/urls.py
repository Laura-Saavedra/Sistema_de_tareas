from django.urls import path
from . import views 
# from usuarios.views import crearUsuario, editarUsuario, loginUsuario, dashboard, perfilUsuarioView, logoutUsuario

# urlpatterns = [
#     path('', loginUsuario),
#     path('crear-usuario/', crearUsuario),
#     path('login/', loginUsuario, name='Login'),
#     path('dashboard/', dashboard),
#     path('perfilUsuario/', perfilUsuarioView.as_view(), name='perfilUsuario'),
#     path('logout/', logoutUsuario, name='logout'),
#     path('editar-usuario/', editarUsuario, name='editarUsuario'),
# ]


urlpatterns = [
    # Raíz → login
    path('', views.loginUsuario, name='Login'),

    # Auth
    path('registro/', views.registroUsuario, name='registro'),
    path('verificar/', views.verificarCorreo, name='verificar_correo'),
    path('reenviar-codigo/', views.reenviarCodigo, name='reenviar_codigo'),
    path('login/', views.loginUsuario, name='Login'),
    path('logout/', views.logoutUsuario, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Perfil
    path('perfil/', views.perfilUsuario, name='perfilUsuario'),
    path('perfil/editar/', views.editarUsuario, name='editarUsuario'),
    path('perfil/password/', views.cambiarPassword, name='cambiarPassword'),
    path('perfil/foto/', views.subirFotoPerfil, name='subirFotoPerfil'),
]