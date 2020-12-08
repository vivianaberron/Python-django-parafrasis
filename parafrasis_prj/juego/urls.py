from django.urls import path

from . import views
from . import forms

urlpatterns = [
    path('textos/', views.buscar_texto_view, name='buscar_texto'),
    path('juego1/', views.juego1_view, name='juego1'),

]