import sys

import typing
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from RegistracijaIgraca import RegistracijaIgraca
from PregledSvihIgraca import PregledSvihIgraca
from Login import Login
from DodavanjePojma import DodavanjePojma


#from UnesiIme import UnesiIme

# Prvi prozor koji se zeli pokrenuti

class Izbornik(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("Izbornik.ui", self)

        self.startGumb.clicked.connect(self.igraj)
        self.RegistracijaIgracaGumb.clicked.connect(self.registracijaIgraca)
        self.hallOfFameGumb.clicked.connect(self.pregledIgraca)
        self.pojmoviGumb.clicked.connect(self.pojmovi)
        self.izlazGumb.clicked.connect(self.izlaz)



    def igraj(self):
        self.prozorIgranje = Login()
        self.prozorIgranje.show()

    def pregledIgraca(self):
        self.pregledIgraca = PregledSvihIgraca()
        self.pregledIgraca.show()
    

    def registracijaIgraca(self):
        self.registracija = RegistracijaIgraca()
        self.registracija.show()
    
    def pojmovi(self):
        self.izbornikPojmova = DodavanjePojma()
        self.izbornikPojmova.show()


    def izlaz(self):
        self.close()
