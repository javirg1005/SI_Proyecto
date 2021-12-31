# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
#import json

def scraper(categoria):
    
    #noticiasDiarias = 0
    #fechaAnterior = ""

    #Pillar todas las urls en las paginas
    for paginas in range(1,2): #Se empieza a partir de la segunda para facilitar la busqueda por url porque la 1 no tiene numero
            
        # Conseguimos la URL
        url_base = "https://www.elmundo.es/"
        
        url = url_base + categoria #+ "/" + str(paginas)
        
        # Hacemos la petición
        page = requests.get(url)
        #print(page.status_code)    #print del codigo de estado al pillar la url (si falla o no y porque)

        # Imprimimos el contenido de la página
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup) #print del contenido

        articulos = soup.findAll("article")
        urls = []
        
    
        print("URL Pagina: " + url)
        # Aplicamos regex
        for articulo in articulos: #REGEX PARA SACAR LAS URLS DE NOTICAS DE LA PAGINA DE PAGINAS
            regex = '<a class="ue-c-cover-content__link-whole-content" href="(.*?)"' #En proceso
            resultado_regex = re.search(regex, str(articulo))
            if resultado_regex != None:
                urls.append(resultado_regex.group(1))
        #print("Lista de URLS: ")
        print(urls)
        '''   
        if(categoria == 'salud/medicina'):
            categoria = 'salud'
        elif(categoria == 'tecnologia/emprendimiento'):
            categoria = 'tecnologia'    
        '''
        
        # Una vez tenemos la URL de la notica en concreto, la scrapeamos
        for i in range(0, len(urls)):
            noticia = requests.get(urls[i])
            print("NOTICIA: " + str(i))
            print("--------------------------")
            print(urls[i])
            print("--------------------------")
            print(noticia.status_code)

            # Imprimimos el contenido de la página
            soup_noticia = BeautifulSoup(noticia.content, 'html.parser')
            #print(soup_noticia)
            
            regexTitulo = 'js-headline">(.*)<\/h1>'
            regexAutor = '<div class="ue-c-article__byline-name">([\w\W]*?)<\/div>'
            regexFecha = '<time datetime="(.*?)T'
            regexEntradilla = '<p class="ue-c-article__standfirst">(.*?)<\/p>'
            regexCuerpo = '<\/ul><p>(.*)<\/p>'
            
            titulo = re.search(regexAutor, str(soup_noticia))
            #print(titulo)
            titulo = titulo.group(1)
            titulo = re.sub(r'\<.*?\>', '', titulo)
            print(titulo)
            '''
            autor = re.search(regexAutor, str(soup_noticia))
            autor = autor.group(1)
            fecha = re.search(regexFecha, str(soup_noticia))
            fecha = fecha.group(1)
            entradilla = re.search(regexEntradilla, str(soup_noticia))
            entradilla = entradilla.group(1)
            entradilla = re.sub(r'\<.*?\>', '', entradilla)
            parrafos = re.findall(regexCuerpo, str(soup_noticia))
            
            cuerpo = ""
            
            for parrafo in parrafos:
                cuerpo = cuerpo + ' ' + parrafo
            
            cuerpo = re.sub(r'\<.*?\>', '', cuerpo)
            
            print(titulo)
            '''
            '''
            dia = fecha[0:2]
            mes = fecha[3:5]
            anio = fecha[6:10]
            nuevaFecha = anio + "-" + mes + "-" + dia
            separador = "\n#####\n"
            
            if(nuevaFecha != fechaAnterior):
                noticiasDiarias = 1
            else:
                noticiasDiarias = noticiasDiarias + 1
                
        
            fichero = "../noticias/20Minutos/" + categoria + "/" + categoria + "." + nuevaFecha + "." + str(noticiasDiarias).zfill(3) + ".txt"
            
            file = open(fichero, "w+", encoding="utf-8")
            file.write(urls[i])
            file.write(separador)
            file.write(autor)
            file.write(separador)
            file.write(nuevaFecha)
            file.write(separador)
            file.write(titulo)
            file.write(separador)
            file.write(entradilla)
            file.write(separador)
            file.write(cuerpo)
            file.close()
            
            fechaAnterior = nuevaFecha
            '''
            print("\n")
            

def scrapeo_init():
    categorias = ['ciencia-y-salud/ciencia.html'] #Categorias a revisar, mirar que esten asi en el periodico (url)
    for categoria in categorias:
        
        scraper(categoria) #Tiene que ser en minuscula
        
    return 0

json_final = scrapeo_init()

print(json_final)

