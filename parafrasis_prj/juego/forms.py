from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Texto


def getOpciones():
    textos = Texto.objects.all()
    opciones=[]
    for t in textos:
        opciones.append((t.titulo,t.titulo))
    return opciones

class Buscar_texto_form(forms.Form):
    texto = forms.CharField(label='Texto deseado?', widget=forms.Select(choices=getOpciones()))    
    # texto = forms.CharField(max_length=30,label='Textow')

class juego1_0_form(forms.Form):
    #texto = forms.CharField(max_length=30,label='Textow')
    tema = forms.CharField(label='Tema del juego?', widget=forms.Select(choices=getOpciones()))    

class juego1_1_form(forms.Form):
    #texto = forms.CharField(max_length=30,label='Textow')
    texto_jugador = forms.CharField(widget=forms.Textarea)
    


