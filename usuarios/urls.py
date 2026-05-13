from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from usuarios.views import crearUsuario,loginUsuario,dashboard,ListaUsuariosView

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        loginUsuario
    ),

    path(
        'crear-usuario/',
        crearUsuario
    ),
    path(
    'login/',
    loginUsuario
    ),
    path(
    'dashboard/',
    dashboard
    ),
    path(
    'lista-usuarios/',
    ListaUsuariosView.as_view(), name='listarUsuarios'
    ),
]