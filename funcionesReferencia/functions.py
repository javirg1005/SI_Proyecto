import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')



## -- Preprocesamiento del texto -- ##

################################################
##Version muchos archivos .txt en una carpeta ##
################################################

#Fuente: https://github.com/javirg1005/PC1_Final/blob/master/tratamientoDelLenguaje.py



def limpieza(lista_textos):
    # Declaramos las stopwords
    lista_stopwords = set(stopwords.words('spanish'))    
    lista_tokens = []

    for txt in lista_textos:        
        # Limpieza del texto
        txt = re.sub('[%s]'  % re.escape(string.punctuation + "'" + '"' + "’" + '”' + '“' + "•‘"), ' ', str(txt)) 
        txt = txt.lower() 
        txt = re.sub('\w*\d\w*', ' ', str(txt))
        
        # Tokenizamos por palabra
        txt = word_tokenize(str(txt))        
        tokens = []

        # Quitamos las stopwords
        for w in txt:
            if not w in lista_stopwords:
                tokens.append(w)        
        lista_tokens.append(tokens)    
    return lista_tokens

# Estemización
def estemizar(lista_tokens):    
    lista_estemizados = []
    for token in lista_tokens:
        token_stem = []
       
        for t in token:
            t = nltk.stem.SnowballStemmer('spanish').stem(t)
            token_stem.append(t)
        lista_estemizados.append(token_stem)
    return lista_estemizados

# Destokenizamos
def destokenizar(token_list):
    aux_list = []
    for token in token_list:
        token = TreebankWordDetokenizer().detokenize(token)
        aux_list.append(token)
    return aux_list

####################################
## Version simple para un archivo ##
####################################

#Fuente: https://github.com/javirg1005/PVA_SI/Audio.py

def limpiar(text):
    sw = set(stopwords.words("spanish"))
    # Limpio con regex el texto
    text = re.sub('[%s]' % re.escape(string.punctuation + "'" + '"' + "’" + '”' + '“' + "•‘"), ' ', str(text))
    text = re.sub('\w*\d\w*', ' ', str(text))
    # Pongo el texto en minúsculas
    text = text.lower()
    # Tokenizo por palabras
    text = word_tokenize(str(text))
    tokens = []
    for t in text:
        if not t in sw:
            tokens.append(t)
    return tokens

def estemizar(token_list):
    new_token = []
    for token in token_list:
        token = SnowballStemmer('spanish').stem(token)
        new_token.append(token)
    return new_token

