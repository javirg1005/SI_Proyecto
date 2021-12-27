import re
import requests
from bs4 import BeautifulSoup
#import json

def scraper(categoria):
    
    noticiasDiarias = 0
    fechaAnterior = ""

    #Pillar todas las urls en las paginas
    for paginas in range(2,4): #Se empieza a partir de la segunda para facilitar la busqueda por url porque la 1 no tiene numero
            
        # Conseguimos la URL
        url_base = "https://www.20minutos.es/"
        
        url = url_base + categoria + "/" + str(paginas)
        
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
            regex = '<header><h1><a href="(.*?)">' #En proceso
            resultado_regex = re.search(regex, str(articulo))
            if resultado_regex != None:
                urls.append(resultado_regex.group(1))
        #print("Lista de URLS: ")
        #print(urls)
            
                
        
        ######Conseguir las url_noticia de las pagina
        #url_20mins = "https://www.20minutos.es/"
        #noticias = []
        '''
        for i in range (len(urls)):
            url_noticia = url_20mins + urls[i]
            print(url_noticia)
            noticias.append(url_noticia)
        '''

        # Una vez tenemos la URL de la notica en concreto, la scrapeamos
        for i in range(0, len(urls)):
            noticia = requests.get(urls[i])
            print("NOTICIA: " + str(i))
            print("--------------------------")
            print(urls[i])
            print("--------------------------")
            #print(noticias.status_code)

            # Imprimimos el contenido de la página
            soup_noticia = BeautifulSoup(noticia.content, 'html.parser')
            #print(soup_noticia)

            # Se escribe en un archivo la salida del HTML de la noticia para poder pasarlo a regex más fácilmente
            #file = open("html_noticia.txt", "w+", encoding="utf-8")
            #file.write(str(soup_noticia))
            #file.close()
            

            ## ------------ Información por cada noticia --------------- ##

            # Inicialización de variables para prevenir errores
            #titulo = "Título no disponible"
            #cuerpo = "Cuerpo de la noticia"
            
            regexTitulo = 'itemprop="headline">(.*)<\/h1>'
            regexAutor = '<strong>(.*?)<\/strong>'
            regexFecha = '"article-date">[\w\W]*?>(.*?)<'
            regexEntradilla = '<div class="article-intro[\w\W]*?>[\w\W]*?>(.*)<\/div>'
            regexCuerpo = '<p class="paragraph[\w\W]*?>(.*?)<\/p>'
            
            titulo = re.search(regexTitulo, str(soup_noticia))
            titulo = titulo.group(1)
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
            
            print("\n")
        #return json_string
'''
            # Título
            regexTitulo = 'itemprop="headline">(.*)<\/h1>' #Regex perron que saque el titulo
            if str(soup_noticia).find("tit"):
                titulo = re.search(regexTitulo, str(soup_noticia))
                if titulo != None:
                    titulo = titulo.group(1)
                else:
                    titulo = "Título no disponible"    
            else:
                titulo = "Título no disponible"
            print("Titulo:")
            print(titulo)

            # Descripción
            regexCuerpo = '<p class="paragraph[\w\W]*?>(.*?)<\/p>' #Regex perron que saque el cuerpo
            if str(soup_noticia).find("DetailDescription"):
                cuerpo = re.search(regexCuerpo, str(soup_noticia))
                if cuerpo != None:
                    cuerpo = cuerpo.group(1)
                    cuerpo = re.sub(r'\<.*?\>', '', cuerpo)
                else:
                    print("cuerpo no encontrada")
            else:
                cuerpo = "Descripción no disponible"
            print("Cuerpo:")
            #print(cuerpo, end= "\n") 

            data = {} #Escribir estructura del json bonito :D
            json_string.append(data)
            #print(data)
            print("\n")
        return json_string
    '''
      
# Se crea el JSON

def scrapeo_init():
    categorias = ['ciencia'] #Categorias a revisar, mirar que esten asi en el periodico (url)
    #json_final = []
    for categoria in categorias:
        #print(categoria)
        scraper(categoria) #Tiene que ser en minuscula
        #json_final.append(json)
    #return json_final
    return 0

#json_final = scrapeo_init() #Tiene que ser en minuscula
json_final = scrapeo_init()

print(json_final)
'''
#Para guardarlo bonito :D
with open('textos/20mins.json', 'w', encoding='utf-8') as f:
    json.dump(json_final, f, ensure_ascii=False, indent=4)
    '''

