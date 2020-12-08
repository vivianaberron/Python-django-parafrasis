
from django.shortcuts import redirect, render
from django.http import HttpResponse
import random 

from .models import Texto, Oracion, Palabra
from .forms import Buscar_texto_form, juego1_0_form, juego1_1_form

def buscar_texto_view(request):
    context = {
        'submitted':False,
        'texto' : '',
        'forma': Buscar_texto_form,
    }
    if request.method == 'POST':
        #context['submitted'] = request.POST['submitted'],
        #https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4
        busqueda = request.POST['texto'].strip()
        context['submitted'] = True
        context['texto'] =  Texto.objects.get(titulo=busqueda)
        return render(request,"texto.html",context=context)
    if 'submitted' in request.POST:
        context['submitted'] = True
    return render(request,"texto.html",context=context)
from django.http import HttpResponseRedirect
from django.views import generic


def setSessionProyectoActual(request,context,pk=0):
    context['proyecto_actual'] = pk
    request.session['proyecto_actual'] = pk

def getSessionProyectoActual(request):
    return request.session.get('proyecto_actual',0)

def juego1_view(request):
    context = {
        'submitted':False,
        'forma': juego1_0_form,
    }

    context['texto'] =  ''
    if request.method == 'POST':
        #context['submitted'] = request.POST['submitted'],
        #https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4
        if 'nivel' in request.session:
            request.session['nivel'] += 1
            tema = request.session['tema']
            texto_jugador = request.POST['texto_jugador'].strip()
            palabras = request.session['palabras']
            context['texto_jugador'] = texto_jugador
        else:
            request.session['nivel'] = 1 
            tema = request.POST['tema']
            request.session['tema'] = tema
            palabras = Texto.objects.get(titulo=tema).getTodasLasPalabras()
            request.session['palabras'] = palabras

        context['tema'] = tema
        context['nivel'] = request.session['nivel']
        if context['nivel']<=3:
            context['palabras'] = palabras
            context['prueba'] = random.sample(palabras,7)
        elif context['nivel']==4:
            oraciones = Texto.objects.get(titulo=tema).getOraciones().values('id')
            nivel2 = []
            for k in random.sample(range(0,oraciones.count()),2):
                prueba = []
                for p in Oracion.objects.get(id=k).getPalabras()[0:7]:
                    prueba.append(p.lemma)
                nivel2.append(prueba)
            request.session['nivel2'] = nivel2
        elif context['nivel']==6:
            return render(request,"juegoFin.html",context=context) 
            
        if context['nivel']>=4:
            context['nivel2'] = request.session['nivel2']
        context['submitted'] = True
        context['forma'] = juego1_1_form
        # levanta una excepcio
        #request.session['error'] = request.session['error'] 
        return render(request,"juego1.html",context=context)
    elif request.method == 'GET':
        if 'nivel' in request.session:
            del request.session['nivel']
        if 'tema' in request.session:
            del request.session['tema']
    return render(request,"juego1.html",context=context)

