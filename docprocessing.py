import string
import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')
# nltk.download('stopwords')

def read_docs():
    token_dict = {}
    # I get the absolute path of the current file to get the path of the directory of the project
    absolute_path = os.path.abspath(__file__)
    project_dir_path = os.path.dirname(absolute_path)
    # I use the project directory path to build the path for the news folder
    news_path = project_dir_path + "\\noticias"
    # I navigate through the directories to get all news files
    for dirpath, dirs, files in os.walk(news_path):
        for f in files:
            fname = os.path.join(dirpath, f)
            print("fname=", fname)
            with open(fname, encoding="utf-8") as pearl:
                text = pearl.read().lower()
                token_dict[f] = re.sub("[" + string.punctuation + "¿¡“”]", "", text)

    return token_dict

def tokenize_and_stem(text):
    f = open("lista_parada.txt", "r", encoding="utf-8",)
    stop_words = f.read().split('\n')
    f.close()
    # Tokenize and filter stop words
    tokens = [x for x in word_tokenize(text) if x not in stop_words]
    stems = []
    stemmer = SnowballStemmer("spanish")
    #Stemming
    for item in tokens:
        stems.append(stemmer.stem(item))
    return stems
    

#calling the TfidfVectorizer
vectorize= TfidfVectorizer(tokenizer = tokenize_and_stem)
#fitting the model and passing our sentences right away:
docs = read_docs()
response = vectorize.fit_transform(docs.values())
#response= vectorize.fit_transform([firstV, secondV])

feature_names = vectorize.get_feature_names()
wordlist = ""
for col in response.nonzero()[1]:
    #print(feature_names[col], ' - ', response[0, col])
    wordlist += feature_names[col]+"\n"

# MAKE DATAFRAME WITH DOCS AND WORDS TD-IDF 
df_tfidfvect = pd.DataFrame(data = response.toarray(),index = docs.keys(), columns = feature_names)

print("\nTD-IDF Vectorizer\n")
print(df_tfidfvect)

# Save wordlist 
'''f = open("wordlist.txt", "w", encoding="utf-8")
f.write(wordlist)
f.close()'''
