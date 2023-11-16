import sqlite3
import sys
import random
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#from Igranje import Igranje
from Igranje_WheelOfFortune import Igranje
#from Igranje import Igranje



class Login(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("Login.ui", self)
        self.aktivni=[]

        self.pokreniIgruGumb.clicked.connect(self.logiraj)
        self.povratakGumb.clicked.connect(self.povratak)

    def logiraj(self):
        igraciTuple = None
        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            igraciTuple = naredbe.execute("SELECT Username FROM Igraci;").fetchall()

        registriraniIgraci = [igrac[0] for igrac in igraciTuple] #Vadi playere iz tupple, tupple je ono sto dobijemo iz baze

        uneseniIgraci = [
        self.username1Text.text().strip(),
        self.username2Text.text().strip(),
        self.username3Text.text().strip(),
        self.username4Text.text().strip(),
        self.username5Text.text().strip(),
        ]
    
        provjeraUnesenihIgraca = []
    
        for username in uneseniIgraci:
            if username != "":
                if username in registriraniIgraci:
                    provjeraUnesenihIgraca.append(username)
                    
                else:
                    self.__porukaProzor(f"{username} korisnik nije registriran")

        
        '''for username in uneseniIgraci:
            if username != "":
                if username in registriraniIgraci:
                    if username in provjeraUnesenihIgraca:
                        self.__porukaProzor(f"{username} je već unesen")
                    else:
                        provjeraUnesenihIgraca.append(username)
                    
                else:
                    self.__porukaProzor(f"{username} korisnik nije registriran")'''
                 

        # Provjerimo jel ima bar 2 unesena usernama
        if len(provjeraUnesenihIgraca) >= 2:
            self.aktivni = provjeraUnesenihIgraca
            self.igra = Igranje(self.aktivni)
            self.igra.show()
            self.close()
        else:
            self.__porukaProzor("Minimalno dva igraca")

    #TODO Što ako ne unese registriranog igrača 

    def __porukaProzor(self,poruka:str,stoJe="warning"):
        '''Privatna je metode, koristit cemo je samo u ovoj klasi za ispisivanje poruka u slucaju
        pogreske'''
        porukaProzor = QMessageBox()
        if stoJe=="warning":
            porukaProzor.setIcon(QMessageBox.Warning)
        else:
            porukaProzor.setIcon(QMessageBox.Information)
        porukaProzor.setText(poruka)
        porukaProzor.setStandardButtons(QMessageBox.Ok) #gumb, gumbi se mogu okomitom crtom odvajati

        porukaProzor.exec() #pokazati poruku

    '''def pokreniIgru(self):
        self.logiraj()
        self.igra= Igranje(self.aktivni)
        self.igra.show()'''


    def povratak(self):
        self.close()