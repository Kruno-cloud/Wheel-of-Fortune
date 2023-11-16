from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3

class PregledSvihIgraca(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("PregledSvihIgraca.ui",self)

        #IGRAC TRAZI: (self,USERNAM, ime:str,prezime:str, lozinka: str, datumRodenja:str, oib:str,drzavljanstvo:str,spol:str, )
       
        igraci = None
        with sqlite3.connect("BazaIgraca.db") as conn: 
            naredbe = conn.cursor()
            igraci=naredbe.execute("SELECT * FROM Igraci;").fetchall()
            
        self.igraciTable.setRowCount(len(igraci)+1) #plus jedan je zbog headera
        self.igraciTable.setItem(0,0,QTableWidgetItem("USERNAME")) #Prvi redak i prvi stupac
        self.igraciTable.setItem(0,1,QTableWidgetItem("IME"))
        self.igraciTable.setItem(0,2,QTableWidgetItem("PREZIME"))
        self.igraciTable.setItem(0,3,QTableWidgetItem("DATUM ROĐENJA"))
        self.igraciTable.setItem(0,4,QTableWidgetItem("OIB"))
        self.igraciTable.setItem(0,5,QTableWidgetItem("DRŽAVLJANSTVO"))
        self.igraciTable.setItem(0,6,QTableWidgetItem("SPOL"))

        redak=1
        
        for sudionik in igraci: #ispisuje tupple
            self.igraciTable.setItem(redak,0,QTableWidgetItem(sudionik[0])) #Prvi redak i prvi stupac
            self.igraciTable.setItem(redak,1,QTableWidgetItem(sudionik[1]))
            self.igraciTable.setItem(redak,2,QTableWidgetItem(sudionik[2]))
            self.igraciTable.setItem(redak,3,QTableWidgetItem(sudionik[4]))
            self.igraciTable.setItem(redak,4,QTableWidgetItem(sudionik[5]))
            self.igraciTable.setItem(redak,5,QTableWidgetItem(sudionik[6]))
            self.igraciTable.setItem(redak,6,QTableWidgetItem(sudionik[7]))


            redak+=1


        self.povratakGumb.clicked.connect(self.zatvoriMe)
    
    def zatvoriMe(self):
        self.close()