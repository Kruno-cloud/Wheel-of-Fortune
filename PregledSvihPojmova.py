from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3

class PregledSvihPojmova(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("PregledSvihPojmova.ui",self)

        #IGRAC TRAZI: (self,ime:str,prezime:str,username:str, lozinka: str, datumRodenja:str, oib:str,drzavljanstvo:str,spol:str, )
       
        pojamKategorija = None
        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            self.pojamKategorija = naredbe.execute("SELECT poi.Naziv, Kat.Naziv as kategorija FROM Pojmovi poi INNER JOIN Kategorije Kat ON poi.idKategorija = Kat.id;").fetchall()
        

        self.pojam = self.pojamKategorija[0]

        self.kategorija=self.pojamKategorija[1]
            
        self.pojmoviTable.setRowCount(len(self.pojamKategorija)+1) #plus jedan je zbog headera
        self.pojmoviTable.setItem(0,0,QTableWidgetItem("Naziv")) #Prvi redak i prvi stupac
        self.pojmoviTable.setItem(0,1,QTableWidgetItem("Kategorija"))
  
        redak=1
        
        for clan in self.pojamKategorija: #ispisuje tupple
            self.pojmoviTable.setItem(redak,0,QTableWidgetItem(clan[0])) #Prvi redak i prvi stupac
            self.pojmoviTable.setItem(redak,1,QTableWidgetItem(clan[1]))



            redak+=1


        self.povratakGumb.clicked.connect(self.zatvoriMe)
    
    def zatvoriMe(self):
        self.close()