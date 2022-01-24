import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
#import re
import os
#import pickle

from modelo.DocProcessing import DocProcessing

class MyWindow(QtWidgets.QMainWindow):

    #El orden importa, para cargar datos importa, aqui cargar los combobox
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('./main.ui',self)    

        self.fill_combobox()
        self.ranking_paths = []
        # Cargar los documentos procesados para que sea más rapido
        '''pickle_in = open('modelo\docsprocessed.pickle', 'rb')
        self.process = pickle.load(pickle_in)'''

        #Si da el error comentar 20,21 y descomentar 24
        self.process = DocProcessing()

        '''with open('modelo/docsprocessed.pickle', 'wb') as f:
            pickle.dump(self.process, f)'''
        

    def fill_combobox(self):
        self.cb_fuente.addItems(["Escoger fuente", "20 minutos", "El Mundo", "El Pais"])
        self.cb_filtro_fuente.addItems(["Escoger fuente", "20 minutos", "El Mundo", "El Pais"])
        self.cb_filtro_fuente_1.addItems(["Escoger fuente", "20 minutos", "El Mundo", "El Pais"])
        self.cb_category.addItems(["Escoger categoría", "ciencia", "salud", "tecnologia"])
        self.cb_filtro_categ.addItems(["Escoger categoría", "ciencia", "salud", "tecnologia"])
        self.cb_new.addItem("Escoger noticia")
        self.cb_top.addItems(['1','3','5','7','8','10','12','15','18','20'])
        self.cb_top_1.addItems(['1','3','5','7','8','10','12','15','18','20'])

        self.cb_fuente.currentTextChanged.connect(self.fill_cb_news_files)
        self.cb_category.currentTextChanged.connect(self.fill_cb_news_files)
        self.cb_new.currentTextChanged.connect(self.on_cb_new_changed)
        self.btn_search.clicked.connect(self.search_callback)
        self.btn_recommend.clicked.connect(self.recomend_callback)
        self.btn_search_1.clicked.connect(self.search_1_callback)
        self.ql_ranking_1.itemClicked.connect(self.ranking_clicked)
        self.ql_ranking_2.itemClicked.connect(self.ranking_clicked_2)

    def fill_cb_news_files(self):
        # fill every news txt name
        fuente = self.getFuente(self.cb_fuente.currentText())
        categoria = self.cb_category.currentText()
        if (fuente == "Escoger fuente" or categoria == "Escoger categoría"):
            self.tx_preview.clear()
            self.cb_new.clear()
            self.cb_new.addItem("Escoger noticia")
        else:
            self.tx_preview.clear()
            self.cb_new.clear()
            self.cb_new.addItem("Escoger noticia")
            file_dir_path = os.path.dirname(__file__)
            for dirpath, dirs, files in os.walk(file_dir_path + "\\noticias\\"+ fuente + "\\" + categoria):
                for f in files:
                    self.cb_new.addItem(f)
            

    def on_cb_new_changed(self, value):
        fuente = self.getFuente(self.cb_fuente.currentText()) 
        categoria = self.cb_category.currentText()
        if (value == "Escoger noticia" or fuente == "Escoger fuente" or categoria == "Escoger categoría" or value == ""):
            self.tx_preview.clear()
        else:
            print("combobox changed", value)
            self.tx_preview.clear()
            path = "./noticias/" + fuente + '/'+ categoria + '/'+ value
            with open(path, encoding="utf-8") as pearl:
                text = pearl.read()
            self.tx_preview.insertPlainText(text)

    def search_callback(self):
        #PONER LA FUNCION DE BUSCAR SEGUN LA NOTICIA (punto 2)
        query = self.tx_preview.toPlainText()
        self.tx_noticia.clear()
        if query != "":
            source_filter = self.getFuente(self.cb_filtro_fuente.currentText()) 
            category_filter = self.cb_filtro_categ.currentText()
            top = int(self.cb_top.currentText())
            self.ql_ranking_2.clear()
            self.ranking_paths.clear()
            # Si ha escogido filtro ambos filtros
            if source_filter != "Escoger fuente" and category_filter != "Escoger categoría":
                sim = self.process.query_sim_ranking_source_category_filtered(query, top, source_filter, category_filter, modo='d')
            elif source_filter != "Escoger fuente":
                sim = self.process.query_sim_ranking_source_filtered(query, top, source_filter, modo= 'd')
            elif category_filter != "Escoger categoría":
                sim = self.process.query_sim_ranking_category_filtered(query, top, category_filter, modo='d')
            else:
                sim = self.process.query_sim_ranking(query, top, modo= 'd')

            for key in list(sim.keys()):
                    self.ranking_paths.append(str(key))
                    text = str(key).split('\\').pop() + ' (' + str(round(sim[key]*100, 2)) + '%)'
                    item = QtWidgets.QListWidgetItem(text)
                    self.ql_ranking_2.addItem(item)

    def recomend_callback(self):
        query = self.tx_preview.toPlainText()
        self.tx_noticia.clear()
        if query != "":
            source_filter = self.cb_filtro_fuente.currentText()
            category_filter = self.cb_filtro_categ.currentText()
            top = int(self.cb_top.currentText())
            self.ql_ranking_2.clear()
            self.ranking_paths.clear()
            # Si ha escogido filtro ambos filtros
            if source_filter != "Escoger fuente" and category_filter != "Escoger categoría":
                sim = self.process.query_sim_ranking_source_category_filtered(query, top, source_filter, category_filter, modo='d')
                self.tx_noticia.insertPlainText("La funcionalidad de recomendaciones no soporta filtros")
            elif source_filter != "Escoger fuente":
                sim = self.process.query_sim_ranking_source_filtered(query, top, source_filter, modo= 'd')
                self.tx_noticia.insertPlainText("La funcionalidad de recomendaciones no soporta filtros")
            elif category_filter != "Escoger categoría":
                sim = self.process.query_sim_ranking_category_filtered(query, top, category_filter, modo='d')
                self.tx_noticia.insertPlainText("La funcionalidad de recomendaciones no soporta filtros")
            else:
                new = self.cb_new.currentText()
                id = self.process.get_pos(new)
                reco = self.recomendation_tags(id)
                reco = self.process.query_reco_ranking(query, top, reco)
                for key in list(reco.keys()):
                    self.ranking_paths.append(str(key))
                    text = str(key).split('\\').pop() + ' (' + str(round(reco[key]*100, 2)) + '%)'
                    item = QtWidgets.QListWidgetItem(text)
                    self.ql_ranking_2.addItem(item)


    def search_1_callback(self):
        #PONER LA FUNCION DE BUSCAR SEGUN QUERY (punto 1)
        query = self.tx_query.toPlainText()
        self.tx_noticia_1.clear()
        if query != "":
            source_filter = self.getFuente(self.cb_filtro_fuente_1.currentText()) 
            top = int(self.cb_top_1.currentText())
            self.ql_ranking_1.clear()
            self.ranking_paths.clear()
            # Si no ha escogido filtro
            if source_filter == "Escoger fuente":
                sim = self.process.query_sim_ranking(query, top, modo ='b')
            else:
                sim = self.process.query_sim_ranking_source_filtered(query, top, source_filter)
            
            for key in list(sim.keys()):
                    self.ranking_paths.append(str(key))
                    text = str(key).split('\\').pop() + ' (' + str(round(sim[key]*100, 2)) + '%)'
                    item = QtWidgets.QListWidgetItem(text)
                    self.ql_ranking_1.addItem(item)

    def ranking_clicked(self, item):
        item_ind = self.ql_ranking_1.row(item)
        self.tx_noticia_1.clear()
        print('item clicked:',self.ranking_paths[item_ind] )
        with open(self.ranking_paths[item_ind], encoding="utf-8") as pearl:
                text = pearl.read()
        self.tx_noticia_1.insertPlainText(text)

    def ranking_clicked_2(self, item):
        item_ind = self.ql_ranking_2.row(item)
        self.tx_noticia.clear()
        print('item clicked:',self.ranking_paths[item_ind] )
        with open(self.ranking_paths[item_ind], encoding="utf-8") as pearl:
                text = pearl.read()
        self.tx_noticia.insertPlainText(text)
    
    def recomendation_tags(self, id):
        #start de recomendation
        tags = self.process.docs_tags #Nos descargamos los tags
        reco = [] #Creamos la lista de resultados
        n = 0 #Contador favorito
        var = 0
        while n != len(tags):
            var1 = tags[id]
            var2 = tags[n]
            var = self.process.dice_coefficient_v2(var1,var2)
            if n == id:
                var = -1 #so it does not recommend itself
            reco.append(var)
            n=n+1
        return reco 

    def getFuente(self, fuente):
        fuente_path = ''
        if(fuente == '20 minutos'):
            fuente_path = '20minutos'
        elif (fuente == 'El Mundo'):
            fuente_path = 'ElMundo'
        elif (fuente == 'El Pais'):
            fuente_path = 'elpais'
        else:
            fuente_path = 'Escoger fuente'

        return fuente_path

    '''
    def dice_coefficient_v2(self,a,b): 
        if not len(a) or not len(b): 
            return 0.0
        if a == b: # quick case for true duplicates
            return 1.0
        if len(a) == 1 or len(b) == 1: 
            return 0.0 # if a != b, and a or b are single chars, then they can't possibly match 
        
        a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
        b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
        
        a_bigram_list.sort()
        b_bigram_list.sort()
        
        # assignments to save function calls
        lena = len(a_bigram_list)
        lenb = len(b_bigram_list)
        # initialize match counters
        matches = i = j = 0
        while (i < lena and j < lenb):
            if a_bigram_list[i] == b_bigram_list[j]:
                matches += 2
                i += 1
                j += 1
            elif a_bigram_list[i] < b_bigram_list[j]:
                i += 1
            else:
                j += 1

        #dice coefficient --> 2nt/(na + nb)
        score = float(matches)/float(lena + lenb) #apply the formula
        return score

    '''
    # para cargar datos importa, aqui cargar los botones

#Método main de la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())