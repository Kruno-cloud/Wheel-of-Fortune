from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Pojam import Pojam

import sqlite3

from PregledSvihPojmova import PregledSvihPojmova

 
class DodavanjePojma(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("DodavanjePojma.ui",self)

        '''
                with open("Studiji.txt","r") as dat:
            studiji = [linija.replace("\n","") for linija in dat.readlines()]
            self.studijiCombo.addItems(studiji)
        
        '''
        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe=conn.cursor()
            dohvaceneKategorije=naredbe.execute(f"SELECT * FROM Kategorije;").fetchall() #Tuples
        
        
        for kategorija in dohvaceneKategorije:
            self.kategorijeComboBox.addItem(kategorija[1],str(kategorija[0])) #dic?? 1. Prikazujem,, a drugo je iza se ne vidi to je u ovom slucaju id


        #kategorije = [kategorija[1] for kategorija in dohvaceneKategorije]
        
        #self.kategorijeComboBox.addItems(kategorije)


        self.unosGumb.clicked.connect(self.unosPojma)
        self.obrisiUnoseGumb.clicked.connect(self.obrisi)
        self.uneseniPojmoviGumb.clicked.connect(self.pregledPojmova)
        self.obrisiPojamGumb.clicked.connect(self.obrisiPojam)

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

    def unosPojma(self):

        naziv = self.nazivText.text().strip()
        opis = self.opisText.toPlainText().strip()
        idKategorije = self.kategorijeComboBox.currentData() #Automobili ((currentData, currentTEXT))

        pojamPostoji = False
    

        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            dohvaceni = naredbe.execute(f"SELECT * FROM Pojmovi WHERE Naziv = '{naziv}';").fetchall() # Trazit cemo ako vec postoji uneseni igrac
            if len(dohvaceni)>0:
                pojamPostoji=True
        
        if pojamPostoji:
            self.__porukaProzor("POGREŠKA! Pojam s tim username-om već postoji!!")
            
        elif pojamPostoji:
            self.__porukaProzor("POGREŠKA! Pojam s tim OIB-om već postoji!!")
        #IGRAC TRAZI: (self,naziv:str,opis:str,username:str, lozinka: str, datumRodenja:str, oib:str,drzavljanstvo:str,spol:str, )
        else:
            try:
                noviPojam = Pojam(naziv, idKategorije, opis)
                
                with sqlite3.connect("BazaIgraca.db") as conn:
                    naredbe= conn.cursor()
                    naredbe.execute(f"INSERT INTO Pojmovi(Naziv, idKategorija, Opis) VALUES('{naziv}', '{idKategorije}', '{opis}')")

                self.__porukaProzor(f"Pojam {noviPojam.naziv} {noviPojam.opis} uspješno unesen!!","information")
            except Exception as exc:
                self.__porukaProzor(str(exc))
        
    def obrisi(self):
        self.nazivText.setText("")
        self.opisText.setPlainText("")
        self.kategorijeComboBox.setCurrentText("Odaberite Kategoriju:")

    def pregledPojmova(self):
        
        
        self.prozorZaPregled = PregledSvihPojmova() 
        self.prozorZaPregled.show()
        '''Kad kreiramo jedan prozor unutar drugoga, ako napravimo show, da nismo postavili self prozor bi se pokazao i nestao bi
        varijabla prozorZaPregled bi postojala samo unutar metode, i nestala bi nakon izlaska iz metode''' 

    def obrisiPojam(self):
        pass #ToDo