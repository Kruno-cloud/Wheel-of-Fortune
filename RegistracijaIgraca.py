from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Igrac import Igrac, datetime
import sqlite3

from PregledSvihIgraca import PregledSvihIgraca
from PretragaIgraca import PretragaIgraca

 
class RegistracijaIgraca(QMainWindow):
    def __init__(self): #Odkud dolaze igraci?
        super().__init__()

        uic.loadUi("RegistracijaIgraca.ui",self)

        self.drzavljanstvoGroup = QButtonGroup()
        self.drzavljanstvoGroup.addButton(self.hrvatskoRadio)
        self.drzavljanstvoGroup.addButton(self.stranoRadio)

        self.spolGroup = QButtonGroup()
        self.spolGroup.addButton(self.muskiRadio)
        self.spolGroup.addButton(self.zenskiRadio)


        '''with open("Studiji.txt","r") as dat:
            studiji = [linija.replace("\n","") for linija in dat.readlines()]
            self.studijiCombo.addItems(studiji)'''
    
        self.unosGumb.clicked.connect(self.unosIgraca)
        self.brisiGumb.clicked.connect(self.obrisi)
        self.pregledUpisanihGumb.clicked.connect(self.pregledIgraca)
        self.pronadjiGumb.clicked.connect(self.pretrazi)

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

    def unosIgraca(self):

        ime = self.imeText.text().strip()
        prezime = self.prezimeText.text().strip()
        username = self.usernameText.text().strip()
        oib = self.oibText.text().strip()
        username = self.usernameText.text().strip()
        lozinka = self.lozinkaText.text().strip()
        datumRodenja=self.dateTimeEdit.text()
        drzavljanstvo = "Hrvatsko"

        if self.stranoRadio.isChecked():
            drzavljanstvo = "Strano"

        spol="Muski"
        if self.zenskiRadio.isChecked():
            spol = "Zenski"


        oibPostoji = False
        usernamePostoji = False

        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            dohvaceni1 = naredbe.execute(f"SELECT * FROM Igraci WHERE username = '{username}';").fetchall() # Trazit cemo ako vec postoji uneseni igrac
            if len(dohvaceni1)>0:
                usernamePostoji=True

            dohvaceni2= naredbe.execute(f"SELECT * FROM Igraci WHERE OIB = '{oib}';").fetchall()
            if len(dohvaceni2)>0:
                oibPostoji=True
        
        if usernamePostoji:
            self.__porukaProzor("POGREŠKA! Igrac s tim username-om već postoji!!")
            
        elif oibPostoji:
            self.__porukaProzor("POGREŠKA! Igrac s tim OIB-om već postoji!!")
        #IGRAC TRAZI: (self,ime:str,prezime:str,username:str, lozinka: str, datumRodenja:str, oib:str,drzavljanstvo:str,spol:str, )
        else:
            try:
                noviIgrac = Igrac(ime, prezime, username, lozinka, datumRodenja, oib, drzavljanstvo, spol)
                
                with sqlite3.connect("BazaIgraca.db") as conn:
                    naredbe= conn.cursor()
                    naredbe.execute(f"INSERT INTO Igraci(username, Ime, Prezime, Lozinka, 'Datum Rodenja', OIB, Drzavljanstvo, Spol) VALUES('{username}', '{ime}', '{prezime}', '{lozinka}', '{datumRodenja}', '{oib}', '{drzavljanstvo}', '{spol}')")

                self.__porukaProzor(f"Igrac {noviIgrac.ime} {noviIgrac.prezime} uspješno unesen!!","information")
            except Exception as exc:
                self.__porukaProzor(str(exc))
        
    def obrisi(self):
        self.imeText.setText("")
        self.prezimeText.setText("")
        self.oibText.setText("")

        self.usernameText.setText("")
        self.lozinkaText.setText("")
        self.oibText.setText("")
        self.hrvatskoRadio.setChecked(True)

        self.stranoRadio.setChecked(False)
        self.muskiRadio.setChecked(True)

        self.zenskiRadio.setChecked(False)

        #self.studijiCombo.setCurrentText("Odaberite studij:")

    def pregledIgraca(self):
        self.prozorZaPregled = PregledSvihIgraca() 
        self.prozorZaPregled.show()
        '''Kad kreiramo jedan prozor unutar drugoga, ako napravimo show, da nismo postavili self prozor bi se pokazao i nestao bi
        varijabla prozorZaPregled bi postojala samo unutar metode, i nestala bi nakon izlaska iz metode''' 

    def pretrazi(self):
        self.prozorZaPretragu = PretragaIgraca()
        self.prozorZaPretragu.show()
