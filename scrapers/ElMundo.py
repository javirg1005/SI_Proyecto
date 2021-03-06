# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
#import json

def scraper(categoria):
    
    noticiasDiarias = 0
    fechaAnterior = ""

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
        #print (articulos[1])
        
    
        print("URL Pagina: " + url)
        # Aplicamos regex
        for articulo in articulos: #REGEX PARA SACAR LAS URLS DE NOTICAS DE LA PAGINA DE PAGINAS
            regex = 'link" href="(.*?)"' #En proceso
            resultado_regex = re.search(regex, str(articulo))
            if resultado_regex != None:
                urls.append(resultado_regex.group(1))
        #print("Lista de URLS: ")
        #print(urls)
         
        if(categoria == 'ciencia-y-salud/ciencia.html'):
            categoria = 'ciencia'
        elif(categoria == 'ciencia-y-salud/salud.html'):
            categoria = 'salud' 
        elif(categoria == 'tecnologia.html'):
            categoria = 'tecnologia'
        
        
        # Una vez tenemos la URL de la notica en concreto, la scrapeamos
        for i in range(0, len(urls)):
            noticia = requests.get(urls[i])
            #print(noticia.content)
            print("NOTICIA: " + str(i))
            print("--------------------------")
            print(urls[i])
            print("--------------------------")
            #print(noticia.status_code)

            # Imprimimos el contenido de la página
            soup_noticia = BeautifulSoup(noticia.content, 'html.parser')
            #print(soup_noticia())
            #file = open('noticiaprueba.txt', "w+", encoding="utf-8")
            #file.write(str(soup_noticia))
            #file.close()
            #print("impreso")
            #print(soup_noticia)
            
            regexTitulo = '<h1[\w\W]*?>(.*?)<\/h1>'
            regexAutor = '<div class="ue-c-article__byline-name">([\w\W]*?)<\/div>'
            regexFecha = '<time datetime="(.*?)T'
            regexEntradilla = '<p class="ue-c-article__standfirst">(.*?)<\/p>'
            regexCuerpo = '<p>(.*?)<\/p>'
            regexTags = 'tags-item"><a href=[\W\w]*?>(.*?)<'
        
            
            titulo = re.search(regexTitulo, str(soup_noticia))
            #if titulo != None:
            titulo = titulo.group(1)
            titulo = re.sub(r'\<.*?\>', '', titulo)
            print(titulo)
            
            autor = re.search(regexAutor, str(soup_noticia))
            if autor != None:
                autor = autor.group(1)
                autor = re.sub(r'\<.*?\>', '', autor)
                autor.replace('\n', '')
                autor.rstrip("\n")
            else:
                autor = ""
            #print(autor)
            
            fecha = re.search(regexFecha, str(soup_noticia))
            if fecha != None:
                fecha = fecha.group(1)
            else:
                fecha = ""
            #print (fecha)
            
            entradilla = re.search(regexEntradilla, str(soup_noticia))
            if entradilla != None:
                entradilla = entradilla.group(1)
                entradilla = re.sub(r'\<.*?\>', '', entradilla)
            else:
                entradilla = ""
            #print (entradilla)
            
            parrafos = re.findall(regexCuerpo, str(soup_noticia))
            if parrafos == None:
                parrafos = ""
            else:
                cuerpo = ""
                for parrafo in parrafos:
                    if cuerpo == "":
                        cuerpo = parrafo
                    else:
                        cuerpo = cuerpo + ' ' + parrafo
                cuerpo = re.sub(r'\<.*?\>', '', cuerpo)
            #print(cuerpo)
            
            tags = re.findall(regexTags, str(soup_noticia))
            if tags == None:
                etiquetas = ""
            else:
                etiquetas = ""
                for tag in tags:
                    if etiquetas == "":
                        etiquetas = tag
                    else:
                        etiquetas = etiquetas + ', ' + tag
                etiquetas = re.sub(r'\<.*?\>', '', etiquetas)
            print(etiquetas)
            
            
                
            '''
            parrafos = re.findall(regexCuerpo, str(soup_noticia))
            if parrafos == None:
                parrafos = ""
            else:
                cuerpo = ""
                for parrafo in parrafos:
                    if cuerpo == "":
                        cuerpo = parrafo
                    else:
                        cuerpo = cuerpo + ' ' + parrafo
                cuerpo = re.sub(r'\<.*?\>', '', cuerpo)
            print(cuerpo)
            '''
            
            if fecha != "":
                separador = "\n#####\n"
                
                if(fecha != fechaAnterior):
                    noticiasDiarias = 1
                else:
                    noticiasDiarias = noticiasDiarias + 1
                    
            
                fichero = "../noticias/ElMundo/" + categoria + "/" + categoria + "." + fecha + "." + str(noticiasDiarias).zfill(3) + ".txt"
                
                file = open(fichero, "w+", encoding="utf-8")
                file.write(urls[i])
                file.write(separador)
                file.write(autor)
                file.write(separador)
                file.write(fecha)
                file.write(separador)
                file.write(titulo)
                file.write(separador)
                file.write(entradilla)
                file.write(separador)
                file.write(cuerpo)
                file.write(separador)
                file.write(etiquetas)
                file.close()
                
                fechaAnterior = fecha
            
            print("\n")
            

def scrapeo_init():
    categorias = ['ciencia-y-salud/ciencia.html', 'ciencia-y-salud/salud.html', 'tecnologia.html'] #Categorias a revisar, mirar que esten asi en el periodico (url)
    for categoria in categorias:
        
        scraper(categoria) #Tiene que ser en minuscula
        
    return 0

json_final = scrapeo_init()

print(json_final)

