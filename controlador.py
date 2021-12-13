import sys
from PyQt5 import QtWidgets, uic
import re
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class MyWindow(QtWidgets.QMainWindow):

    #El orden importa, para cargar datos importa, aqui cargar los combobox

    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('interfaz.ui',self)      

        #hay que ir añadiendo los elementos de la ventana
        #ejemplo:
        #self.cb_fuente.addItems()

    # para cargar datos importa, aqui cargar los botones

#Método main de la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())