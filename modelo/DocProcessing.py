import os
import gensim
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

class DocProcessing:

    def __init__(self):
        f = open("modelo\lista_parada.txt", "r", encoding="utf-8",)
        self.stop_words = f.read().split('\n')
        f.close()
        # read files and store in dic. Then tokenize and stem each one
        self.docs = self.read_docs()
        self.docs_names = list(self.docs.keys())
        self.docs_text = self.docs.values()
        self.docs_stems = self.tokenize_and_stem_docs(self.docs_text)

        # Create dictionary of stems
        self.dictionary = gensim.corpora.Dictionary(self.docs_stems)
        # Store the corpus (bag of words), which contains the words and frecuency in each doc
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs_stems]
        # Convert to td-idf for tokens' weight
        self.tf_idf = gensim.models.TfidfModel(self.corpus)

        # Create a similarity measure object
        self.sims = gensim.similarities.Similarity('modelo\\similarity_object\\', self.tf_idf[self.corpus], num_features=len(self.dictionary))

    def read_docs(self):
        token_dict = {}
        # I get the directory path of the current file to later get the path of the directory of the project
        file_dir_path = os.path.dirname(__file__)
        project_dir_path = os.path.dirname(file_dir_path)
        # I use the project directory path to build the path for the news folder
        news_path = project_dir_path + "\\noticias"
        # I navigate through the directories to get all news files
        for dirpath, dirs, files in os.walk(news_path):
            for f in files:
                fname = os.path.join(dirpath, f)
                #print("fname=", fname)
                with open(fname, encoding="utf-8") as pearl:
                    text = pearl.read()
                    token_dict[fname] = text

        return token_dict

    def tokenize_and_stem_docs(self, docs):
        # Tokenize and filter stop words
        gen_docs = [[w.lower() for w in word_tokenize(text_doc) if w not in self.stop_words] 
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
        query_doc = [w.lower() for w in word_tokenize(query) if w not in self.stop_words]
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

    def query_sim_ranking(self, query, ranking):
        sim = self.query_sim(query)
        rank = sim.argsort()[-ranking:]
        rank_dic = {}
        for i in reversed(rank):
            rank_dic[self.docs_names[i]] = sim[i]

        return rank_dic        


'''process = DocProcessing()
print("ranking")

query = "Saturno es el sexto planeta desde el sol"
print(process.query_sim_ranking(query, 5))

query = "Alexa puede detectar por la voz el estado emocional de los pacientes en algunos hospitales españoles"
print(process.query_sim_ranking(query, 5))
'''