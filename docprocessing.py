import string
import os
import re
import gensim
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

class DocProcessing:

    def __init__(self):
        f = open("lista_parada.txt", "r", encoding="utf-8",)
        self.stop_words = f.read().split('\n')
        f.close()
        # read files and store in dic. Then tokenize and stem each one
        self.docs = self.read_docs()
        self.docs_stems = self.tokenize_and_stem_docs(self.docs.values())

        # Create dictionary of stems
        self.dictionary = gensim.corpora.Dictionary(self.docs_stems)
        # Store the corpus (bag of words), which contains the words and frecuency in each doc
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs_stems]
        # Convert to td-idf for tokens' weight
        self.tf_idf = gensim.models.TfidfModel(self.corpus)

        # Create a similarity measure object
        self.sims = gensim.similarities.Similarity('similarity_object/', self.tf_idf[self.corpus], num_features=len(self.dictionary))s

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

    def tokenize_and_stem_docs(self, docs):
        # Tokenize and filter stop words
        gen_docs = [[w.lower() for w in word_tokenize(text_doc) if w not in self.stop_words + list(string.punctuation) + ['¿','¡','“','”'] ] 
                for text_doc in docs]
        stems = []
        stemmer = SnowballStemmer("spanish")
        #Stemming
        for doc in gen_docs:
            stem_doc = []
            for word in doc:
                stem_doc.append(stemmer.stem(word))
            stems.append(stem_doc)

        return stems

    def tokenize_and_stem_query(self, query):
        # Tokenize and filter stop words
        query_doc = [w.lower() for w in word_tokenize(query) if w not in self.stop_words + list(string.punctuation) + ['¿','¡','“','”']]
        stems = []
        stemmer = SnowballStemmer("spanish")
        #Stemming
        for word in query_doc:
            stems.append(stemmer.stem(word))

        return stems

    def query_sim(self, query):
        #tokenize and stem
        query_stems = self.tokenize_and_stem_query(query)
        #update an existing dictionary and create bag of words
        query_doc_bow = self.dictionary.doc2bow(query_stems) 
        # Convert the bag of words to td-idf for tokens' weight
        query_doc_tf_idf = self.tf_idf[query_doc_bow]
        # perform a similarity query against the corpus
        return self.sims[query_doc_tf_idf]



    #query similirarity
    query = "Saturno es el sexto planeta desde el sol"
    print(query_sim(query, dictionary, sims))

