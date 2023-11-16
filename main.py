import sys
import os


#Tu nam ne treba uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from RegistracijaIgraca import RegistracijaIgraca
from Izbornik import Izbornik
import sqlite3


con = sqlite3.connect("BazaIgraca.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Igraci (username VARCHAR(20) PRIMARY KEY NOT NULL, Ime VARCHAR(20), Prezime VARCHAR(20), Lozinka VARCHAR(20), "Datum Rodenja" VARCHAR(12), OIB CHAR(11) NOT  NULL, Drzavljanstvo VARCHAR(20), Spol VARCHAR(6))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Kategorije (id INTEGER PRIMARY KEY AUTOINCREMENT, Naziv TEXT NOT NULL )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Pojmovi (id INTEGER PRIMARY KEY AUTOINCREMENT, Naziv TEXT NOT NULL, idKategorija INT, Opis TEXT, FOREIGN KEY(idKategorija) REFERENCES Kategorije(id))''')



#The TEXT data type is used to store variable-length character strings of any length.
con.commit()
cur.close()
con.close()

app = QApplication(sys.argv)
prozor = Izbornik()
prozor.show()

# Close the cursor and connection when the application exits
#app.aboutToQuit.connect(lambda: (cur.close(), con.close()))

sys.exit(app.exec())


#Za kasnije
# Odabir kategorije i pojma

'''

SELECT Vozac.ime, Vozac.prezime, Automobili.marka, Automobili.model FROM Vozac, Automobili WHERE Vozac.idAutomobila = Automobili.id;'''

#Kako testirat: INSERT INTO Pojmovi(Naziv,Opis,idKategorija) VALUES ('Tets','Tets',7); Unesi foregin key koji ne pripada kategorije