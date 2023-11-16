import sqlite3
import sys
import random
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Igranje import Igranje


class Login(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("Login.ui", self)
        self.aktivni=[]

        self.pokreniIgruGumb.clicked.connect(self.pokreniIgru)
        self.povratakGumb.clicked.connect(self.povratak)

    def logiraj(self):
        igraciTuple = None
        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            igraciTuple = naredbe.execute("SELECT Username FROM Igraci;").fetchall()

        igraci=[]
        for igrac in igraciTuple:
            igraci.append(igrac[0])


        username1 = self.username1Text.text().strip()
        username2 = self.username2Text.text().strip()
        username3 = self.username3Text.text().strip()
        username4 = self.username4Text.text().strip()
        username5 = self.username5Text.text().strip()

        if username1 != "" and username2 != "":
            if username1 in igraci:
                self.aktivni.append(username1)
            else:
                # Dodati window za prikaz gresku
                self.__porukaProzor(f"{username1} korisnik nije registriran")
            if username2 in igraci:
                self.aktivni.append(username2)
            else:
                # Dodati window za prikaz gresku
                self.__porukaProzor(f"{username2} korisnik nije registriran")
            if username3 != "":
                if username3 in igraci:
                    self.aktivni.append(username3)
                else:
                    self.__porukaProzor(f"{username3} korisnik nije registriran")
            if username4 != "":
                if username4 in igraci:
                    self.aktivni.append(username4)
                else:
                    self.__porukaProzor(f"{username3} korisnik nije registriran")
            if username5 != "":
                if username5 in igraci:
                    self.aktivni.append(username5)
                else:
                    self.__porukaProzor(f"{username3} korisnik nije registriran")
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


    def pokreniIgru(self):
        self.logiraj()
        self.igra= Igranje(self.aktivni)
        self.igra.show()


    def povratak(self):
        self.close()