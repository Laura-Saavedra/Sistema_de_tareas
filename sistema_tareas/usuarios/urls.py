from django.urls import path
from .views import crear_usuario, login_usuario, dashboard, ListaUsuariosView

urlpatterns = [

    path(
        '',
        login_usuario
    ),

    path(
        'crear-usuario/',
        crear_usuario
    ),

    path(
        'login/',
        login_usuario
    ),

    path(
        'dashboard/',
        dashboard
    ),

    path(
        'lista-usuarios/',
        ListaUsuariosView.as_view()
    ),
]
