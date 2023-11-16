from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3

class PretragaIgraca(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("PretragaIgraca.ui",self)


        self.pretragaGumb.clicked.connect(self.pretrazi)
        self.povratakGumb.clicked.connect(self.zatvoriMe)
    
    def __porukaProzor(self,poruka):
        porukaProzor = QMessageBox()
        porukaProzor.setIcon(QMessageBox.Warning)
        porukaProzor.setText(poruka)
        porukaProzor.setStandardButtons(QMessageBox.Ok)
        porukaProzor.exec()

    def __otkljucaj(self):
        self.imeText.setReadOnly(False)
        self.prezimeText.setReadOnly(False)
        self.oibText.setReadOnly(False)
        self.drzavljanstvoText.setReadOnly(False)
        self.usernameText.setReadOnly(False)

    def __zakljucaj(self):
        self.imeText.setReadOnly(True)
        self.prezimeText.setReadOnly(True)
        self.oibText.setReadOnly(True)
        self.drzavljanstvoText.setReadOnly(True)
        self.usernameText.setReadOnly(True)

    def pretrazi(self):
        try:
            sudionik = None
            igraci= None
            with sqlite3.connect("BazaIgraca.db") as conn:
                naredbe=conn.cursor()
                igraci=naredbe.execute(f"SELECT * FROM Igraci WHERE USERNAME = '{self.usernameText.text()}';").fetchall()

            if len(igraci)==0:
                self.__porukaProzor("Student s tim username-om NE POSTOJI!!")

            else:
                self.__otkljucaj()
                sudionik=igraci[0]
                
                #Dobit cemo TUPLE pa zato mozemo traziti stupce po rednom broju
                self.imeText.setText(sudionik[1])
                self.prezimeText.setText(sudionik[2])
                self.oibText.setText(str(sudionik[5]))
                self.drzavljanstvoText.setText(sudionik[6])
                self.datumRodenjaText.setText(sudionik[5])
                self.__zakljucaj()
        except:
            self.__porukaProzor("POGREŠAN UNOS ZA JMBAG!!")

    def zatvoriMe(self):
        self.close()
