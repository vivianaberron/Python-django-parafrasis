from django.db import models
from django.db import IntegrityError

# Create your models here.

class Texto(models.Model):
    titulo = models.CharField(max_length=100,unique=True)
    class Meta:
        ordering = ["titulo"]
    def __str__(self):
        return self.titulo
      
    def getOraciones(self):
        return Oracion.objects.filter(texto=self)

    def getTodasLasPalabras(self):
        palabras = set()
        for oracion in self.getOraciones():
            for palabra in oracion.getPalabras():
                palabras.add(palabra.lemma)
        palabras = list(palabras)
        palabras.sort()
        return palabras

class Oracion(models.Model):
    texto = models.ForeignKey(Texto, on_delete=models.CASCADE)
    oracion = models.TextField(unique=False,blank=False)
    def __str__(self):
        return self.oracion

    def getPalabras(self):
        return Palabra.objects.filter(oracion=self)



class Palabra(models.Model):
    oracion = models.ForeignKey(Oracion,on_delete=models.CASCADE)
    #pos = models.IntegerField()
    lemma = models.CharField(max_length=30)
    tag = models.CharField(max_length=10)
    token = models.CharField(max_length=30)
    categoria = models.CharField(max_length=1)

    def __str__(self):
        return '('+self.lemma+' '+self.tag+' '+self.token+')'

# cargar(titulo="tequila",archivo="textos/tequila.txt")

import requests

def cargar(titulo,archivo,limpiaBase=True):
    print('Procesando:',titulo)
    renglones = []
    # todas = []
    with open(archivo,"r",encoding='utf-8') as file:
        for oracion in file:
            oracion = oracion.strip(' \n')
            with open('borrame.txt',"w",encoding='utf-8') as temp:
                temp.write(oracion)

            files = {'file': open('borrame.txt', 'rb')}
            params = {'outf': 'tagged', 'format': 'json'}
            url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
            r = requests.post(url, files=files, params=params)
            obj = r.json()
 
            print("* ",end='')
            palabrasOracion = []
            for sentence in obj:
                for word in sentence:
                    if word['tag'][0] in ['N','A','R','V','Z']:
                        # http://blade10.cs.upc.edu/freeling-old/doc/tagsets/tagset-es.html
                        # solo se eligen:
                        #    N (Nombres), 
                        #    A (adjetivos)
                        #    R (advervios),
                        #    V (verbos),
                        #    Z (numerales)
                        if not (word['lemma'],word['token'],word['tag']) in palabrasOracion:
                            palabrasOracion.append((word['lemma'],word['token'],word['tag']))
                        # if not (word['lemma'],word['token'],word['tag']) in todas:
                        #    todas.append((word['lemma'],word['token'],word['tag']))
            renglones.append({'oracion':oracion,'palabras':palabrasOracion})

    # todas.sort()

    if limpiaBase:
        Texto.objects.all().delete()
    try:
        texto = Texto.objects.get(titulo=titulo)
            
    except Texto.DoesNotExist:
        texto = Texto.objects.create(titulo=titulo)

    for r in renglones:
        oracion = Oracion.objects.create(texto = texto, oracion = r['oracion'])
        for p in r['palabras']:
            palabra = Palabra.objects.create(oracion=oracion,lemma=p[0],token=p[1],tag=p[2],categoria=p[2][0])
        # print("="*80)
        # print(r['oracion'])
        # print(r['palabras'])

def poblar():
    cargar(titulo="tequila",archivo="textos/tequila.txt",limpiaBase=True)
    cargar(titulo="Kebab",archivo="textos/Kebab.txt",limpiaBase=False)
    cargar(titulo="ofrenda",archivo="textos/ofrenda.txt",limpiaBase=False) 
    cargar(titulo="vegana",archivo="textos/vegana.txt",limpiaBase=False)
    cargar(titulo="camotes",archivo="textos/camotes.txt",limpiaBase=False)
    cargar(titulo="sushi",archivo="textos/sushi0.txt",limpiaBase=False) 