from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('personalizar', views.personalizar, name='personalizar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adicionar_livro/', views.adicionar_livro, name='adicionar_livro'),
    path('buscar/', views.buscar, name='buscar'),
    path('exibir/', views.exibir, name='exibir'),
]