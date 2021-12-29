import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
import re
import os
import pickle

from modelo.DocProcessing import DocProcessing

class MyWindow(QtWidgets.QMainWindow):

    #El orden importa, para cargar datos importa, aqui cargar los combobox
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('./vista/main.ui',self)    

        self.fill_combobox()
        self.ranking_paths = []
        # Cargar los documentos procesados para que sea más rapido
        '''pickle_in = open('docsprocessed.pickle', 'rb')
        self.process = pickle.load(pickle_in)'''
        self.process = DocProcessing()

        '''with open('docsprocessed.pickle', 'rb') as f:
            pickle.dump(self.process, f)'''
        

    def fill_combobox(self):
        self.cb_fuente.addItems(["Escoger fuente", "20minutos", "elmundo", "elpais"])
        self.cb_filtro_fuente.addItems(["Escoger fuente", "20minutos", "elmundo", "elpais"])
        self.cb_filtro_fuente_1.addItems(["Escoger fuente", "20minutos", "elmundo", "elpais", "noticias"])
        self.cb_category.addItems(["Escoger categoría", "ciencia", "salud", "tecnologia"])
        self.cb_filtro_categ.addItems(["Escoger categoría", "ciencia", "salud", "tecnologia"])
        self.cb_new.addItem("Escoger noticia")
        self.cb_top.addItems(['1','3','5','7','8','10','12','15','18','20'])
        self.cb_top_1.addItems(['1','3','5','7','8','10','12','15','18','20'])

        self.cb_fuente.currentTextChanged.connect(self.fill_cb_news_files)
        self.cb_category.currentTextChanged.connect(self.fill_cb_news_files)
        self.cb_new.currentTextChanged.connect(self.on_cb_new_changed)
        self.btn_search.clicked.connect(self.search_callback)
        self.btn_search_1.clicked.connect(self.search_1_callback)
        self.ql_ranking_1.itemClicked.connect(self.ranking_clicked)
        self.ql_ranking_2.itemClicked.connect(self.ranking_clicked_2)

    def fill_cb_news_files(self):
        # fill every news txt name
        fuente = self.cb_fuente.currentText()
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
        fuente = self.cb_fuente.currentText()
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
            source_filter = self.cb_filtro_fuente.currentText()
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

    def search_1_callback(self):
        #PONER LA FUNCION DE BUSCAR SEGUN QUERY (punto 1)
        query = self.tx_query.toPlainText()
        self.tx_noticia_1.clear()
        if query != "":
            source_filter = self.cb_filtro_fuente_1.currentText()
            top = int(self.cb_top_1.currentText())
            self.ql_ranking_1.clear()
            self.ranking_paths.clear()
            # Si no ha escogido filtro
            if source_filter == "Escoger fuente":
                sim = self.process.query_sim_ranking(query, top)
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


    # para cargar datos importa, aqui cargar los botones

#Método main de la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())