# -*- coding: utf-8 -*-
import requests

def cargar(titulo,archivo,limpiaBase=True):
    no=np=ne=0
#    if limpiaBase:
#        if Texto.objects.all().count() > 0:
#            Texto.objects.all().delete()
#    texto = Texto.objects.create(titulo=titulo)


    texto = []
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
            texto.append({'oracion':oracion,'palabras':palabrasOracion})

    # todas.sort()

    for t in texto:
        print("="*80)
        print(t['oracion'])
        print(t['palabras'])
    '''
    for palabra in todas:
        print(palabra)
    print(len(todas))
    '''

cargar('tequila','tequila.txt')