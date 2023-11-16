from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import sqlite3
import random as rnd

# Treci prozor nakon klikanja "Unesi gumba"

class Igranje(QWidget):
    def __init__(self, aktivniIgraci):
        super().__init__()
        self.players=[]
        self.pogodena_slova = []
        self.pokusana_slova = []
        self.trenutniIgrac = 0
        

        for igrac in aktivniIgraci:
            self.players.append({"Username": igrac, "Bodovi": 0})
        
        uic.loadUi("Igranje.ui", self)

        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            pojamKategorija = naredbe.execute("SELECT poi.Naziv, Kat.Naziv as kategorija FROM Pojmovi poi INNER JOIN Kategorije Kat ON poi.idKategorija = Kat.id;").fetchall()
        
        pojamZaPogadanje = rnd.choice(pojamKategorija)
        
        self.pojam = pojamZaPogadanje[0].lower()

        self.pojamBezRazmaka = self.pojam.replace(" ", "")

        self.kategorija=pojamZaPogadanje[1]

        self.prikaziStanje = self.display_puzzle(self.pojam, self.pogodena_slova)
        self.trazenaRijecText.setText(self.prikaziStanje)

        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])
        self.kategorijaEdit.setText(self.kategorija)
        self.provjeraGumb.clicked.connect(self.Pocetak)


    def Pocetak(self):
        
        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])

        pokusajSlova=self.unosSlovaText.text()
        if len(pokusajSlova) == 1:
            if pokusajSlova in self.pokusana_slova and pokusajSlova in self.pogodena_slova:
                QMessageBox.information(self, "Pogreška", "To slovo je pokusano i pogodeno") #Ne radi ako je slovo već pokusano!!
            elif pokusajSlova in self.pokusana_slova:
                QMessageBox.information(self, "Pogreška", "To slovo je pokusano") #Ne radi ako je slovo već pokusano!!
            elif pokusajSlova in self.pojam:
                self.pogodena_slova.append(pokusajSlova)
                self.pokusana_slova.append(pokusajSlova)
                self.prikaziStanje = self.display_puzzle(self.pojam, self.pogodena_slova)
                self.trazenaRijecText.setText(self.prikaziStanje)
            else:
                self.trenutniIgrac = (self.trenutniIgrac + 1) % len(self.players)
        else:
            if pokusajSlova == self.pojam:
                QMessageBox.information(self, "Čestitamo!", f"{self.players[self.trenutniIgrac]['Username']} pogodio je riječ!")

                self.players[self.trenutniIgrac]['Bodovi'] += 1
            else:
                self.trenutniIgrac = (self.trenutniIgrac + 1) % len(self.players)
                
        if(self.prikaziStanje == self.pojam):
            self.show_results(self.players)
        
        self.unosSlovaText.setText("")
        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])

    def display_puzzle(self, word, guesses):
        displayed_word = ""
        for letter in word:
            if letter in guesses:
                displayed_word += letter
            else:
                displayed_word += "_"
        return displayed_word
    
    def show_results(self, players):
        result_message = ""
        for player in players:
            result_message += f"{player['Username']}: {player['Bodovi']}\n"
        QMessageBox.information(self, "Bodovi:", f"{result_message}")


#SELECT poi.Naziv, Kat.Naziv as kategorija FROM Pojmovi poi INNER JOIN Kategorije Kat ON poi.idKategorija = Kat.id
#povezujemo pojmove s kategorijom
#as kategorija je da ne bi imali dva naziva,