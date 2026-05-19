from django.urls import path
from usuarios.views import crearUsuario, editarUsuario, loginUsuario, dashboard, perfilUsuarioView, logoutUsuario

urlpatterns = [
    path('', loginUsuario),
    path('crear-usuario/', crearUsuario),
    path('login/', loginUsuario, name='Login'),
    path('dashboard/', dashboard),
    path('perfilUsuario/', perfilUsuarioView.as_view(), name='perfilUsuario'),
    path('logout/', logoutUsuario, name='logout'),
    path('editar-usuario/', editarUsuario, name='editarUsuario'),
]