import re
import requests
from bs4 import BeautifulSoup
import json

def scraper(categoria):

    json_string = []

    #Pillar todas las urls en las paginas
    for paginas in range(2,200): #Se empieza a partir de la segunda para facilitar la busqueda por url porque la 1 no tiene numero
            
        # Conseguimos la URL
        url_base = "https://www.20minutos.es/"
        
        url = url_base + categoria + "/" + str(paginas) 
        print(url)
        
        # Hacemos la petición
        page = requests.get(url)
        #print(page.status_code)    #print del codigo de estado al pillar la url (si falla o no y porque)

        # Imprimimos el contenido de la página
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup) #print del contenido

        articulos = soup.findAll("article")
        urls = []
    
        print(url)
        # Aplicamos regex
        for articulo in articulos: #REGEX PARA SACAR LAS URLS DE NOTICAS DE LA PAGINA DE PAGINAS
            regex = '<\/div><\/div><div class="media-intro"><ul><li>(.+?)<\/li><li><a href=' #En proceso
            resultado_regex = re.search(regex, str(articulo))
            if resultado_regex != None:
                urls.append(resultado_regex.group(1))
        print(urls)
            
                
        
        ######Conseguir las url_noticia de las pagina
        # Conseguir urls de los pisos
        url_20mins = "https://www.20minutos.es/"
        noticias = []
        
        for i in range (len(urls)):
            url_noticia = url_20mins + urls[i]
            print(url_noticia)
            noticias.append(url_noticia)


        # Una vez tenemos la URL de la notica en concreto, la scrapeamos
        for i in range(0, len(noticias)):
            noticia = requests.get(noticias[i])
            print("--------------------------")
            print(noticias[i])
            print("--------------------------")
            #print(noticias.status_code)

            # Imprimimos el contenido de la página
            soup_noticia = BeautifulSoup(noticia.content, 'html.parser')
            #print(soup_noticia)

            # Se escribe en un archivo la salida del HTML de la noticia para poder pasarlo a regex más fácilmente
            file = open("html_noticia.txt", "w+", encoding="utf-8")
            file.write(str(soup_noticia))
            
            

            ## ------------ Información por cada noticia --------------- ##

            # Inicialización de variables para prevenir errores
            titulo = "Título no disponible"
            cuerpo = "Cuerpo de la noticia"

            # Título
            regexTitulo = '' #Regex perron que saque el titulo
            if str(soup_noticia).find("tit"):
                titulo = re.search(regexTitulo, str(soup_noticia))
                if titulo != None:
                    titulo = titulo.group(1)
                else:
                    titulo = "Título no disponible"    
            else:
                titulo = "Título no disponible"
            print(titulo)

            # Descripción
            regexCuerpo = '' #Regex perron que saque el cuerpo
            if str(soup_noticia).find("DetailDescription"):
                cuerpo = re.search(regexCuerpo, str(soup_noticia))
                if cuerpo != None:
                    cuerpo = cuerpo.group(1)
                    cuerpo = re.sub(r'\<.*?\>', '', cuerpo)
                else:
                    print("cuerpo no encontrada")
            else:
                cuerpo = "Descripción no disponible"
            print(cuerpo, end= "\n") 

            data = {} #Escribir estructura del json bonito :D
            json_string.append(data)
            print(data)
            print("\n")
        return json_string
      
# Se crea el JSON

def scrapeo_init():
    categorias = ['deportes','ciencia'] #Categorias a revisar, mirar que esten asi en el periodico (url)
    json_final = []
    for categoria in categorias:
        print(categoria)
        json = scraper(categoria) #Tiene que ser en minuscula
        json_final.append(json)
    return json_final

json_final = scrapeo_init() #Tiene que ser en minuscula

print(json_final)

#Para guardarlo bonito :D
with open('20mins.json', 'w', encoding='utf-8') as f:
    json.dump(json_final, f, ensure_ascii=False, indent=4)

