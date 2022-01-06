import os
import gensim
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.util import pr

class DocProcessing:

    def __init__(self):
        f = open("modelo\lista_parada.txt", "r", encoding="utf-8",)
        self.stop_words = f.read().split('\n')
        f.close()
        # read files and store in dic. Then tokenize and stem each one
        self.docs = self.read_docs()
        self.docs_names = []
        self.docs_text = []
        for key in self.docs:
            self.docs_names.append(key)
            self.docs_text.append(self.docs[key])

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

    def query_sim_ranking(self, query, ranking, modo ='b'):
        sim = self.query_sim(query)
        if modo == 'b': 
            rank = sim.argsort()[-ranking:]
        else: # modo = 'd'
            rank = sim.argsort()[-ranking-1:-1] # The most similar will be the document itself, so i take it out and retrieve an extra item
        rank_dic = {}
        for i in reversed(rank):
            rank_dic[self.docs_names[i]] = sim[i]

        return rank_dic    
    
    def query_sim_ranking_source_filtered(self, query, ranking, source_filter,  modo ='b'):
        sim = self.query_sim(query)
        if modo == 'b':
            rank = sim.argsort()
        else: #modo = 'd'
            rank = sim.argsort()[:-1] # the most similiar doc will itself so I take it out
        rank_dic = {}
        count = 0
        for i in reversed(rank):
            fuente = self.docs_names[i].split('\\')[-3]
            if (fuente == source_filter and count<ranking):
                rank_dic[self.docs_names[i]] = sim[i]
                count+=1

        return rank_dic

    def query_sim_ranking_category_filtered(self, query, ranking, category_filter, modo = 'b'):
        sim = self.query_sim(query)
        if modo == 'b':
            rank = sim.argsort()
        else: #modo = 'd'
            rank = sim.argsort()[:-1] # the most similiar doc will itself so I take it out
        rank_dic = {}
        count = 0
        for i in reversed(rank):
            categoria = self.docs_names[i].split('\\')[-2]    
            if (categoria == category_filter and count<ranking):
                rank_dic[self.docs_names[i]] = sim[i]
                count+=1

        return rank_dic

    def query_sim_ranking_source_category_filtered(self, query, ranking, source_filter, category_filter,  modo = 'b'):
        sim = self.query_sim(query)
        if modo == 'b':
            rank = sim.argsort()
        else: #modo = 'd'
            rank = sim.argsort()[:-1] # the most similiar doc will itself so I take it out
        rank_dic = {}
        count = 0
        for i in reversed(rank):
            fuente = self.docs_names[i].split('\\')[-3]
            categoria = self.docs_names[i].split('\\')[-2]    
            if (fuente == source_filter and categoria == category_filter and count<ranking):
                rank_dic[self.docs_names[i]] = sim[i]
                count+=1

        return rank_dic
        
            


'''process = DocProcessing()
print("ranking")

query = "Saturno es el sexto planeta desde el sol"
print(process.query_sim_ranking(query, 5))

query = "Alexa puede detectar por la voz el estado emocional de los pacientes en algunos hospitales españoles"
print(process.query_sim_ranking(query, 5))
'''