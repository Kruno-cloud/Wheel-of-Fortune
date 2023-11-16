from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import sqlite3
import random as rnd
import WheelOfFortune



# Treci prozor nakon klikanja "Unesi gumba"

class Igranje(QWidget):
    def __init__(self, aktivniIgraci):
        super().__init__()
        self.players=[]
        self.pogodena_slova = []
        self.pokusana_slova = []
        self.trenutniIgrac = 0
        self.nagrada=None
        

        for igrac in aktivniIgraci:
            self.players.append({"Username": igrac, "Bodovi": 0})
        
        uic.loadUi("Igranje.ui", self)

        with sqlite3.connect("BazaIgraca.db") as conn:
            naredbe = conn.cursor()
            pojamKategorija = naredbe.execute("SELECT poi.Naziv, Kat.Naziv as kategorija FROM Pojmovi poi INNER JOIN Kategorije Kat ON poi.idKategorija = Kat.id;").fetchall()
        
        pojamZaPogadanje = rnd.choice(pojamKategorija)
        
        self.pojamSaRazmakom = pojamZaPogadanje[0].lower()

        self.pojamBezRazmaka = self.pojamSaRazmakom.replace(" ", "")

        self.kategorija=pojamZaPogadanje[1]

        self.prikaziStanje = self.funkcijaZaPrikazStanja(self.pojamSaRazmakom, self.pogodena_slova)
        self.trazenaRijecText.setText(self.prikaziStanje)

        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])
        self.kategorijaEdit.setText(self.kategorija)
        self.provjeraGumb.clicked.connect(self.Pocetak)
        self.kolo = WheelOfFortune #Pomoć
        self.zavrtiKoloGumb.clicked.connect(lambda:WheelOfFortune.paliKolo()) #Pomoć

    def vratiNagradu(self):
        
        return WheelOfFortune.get_nagrada()

    def Pocetak(self):
        
        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])
        #self.bodoviNaReduText.setText(self.players[self.trenutniIgrac]["Bodovi"])

        pokusajSlova=self.unosSlovaText.text()
        if len(pokusajSlova) == 1:
            if pokusajSlova in self.pokusana_slova and pokusajSlova in self.pogodena_slova:
                self.__porukaProzor("Pogreška", "To slovo je pokusano i pogodeno")
                
                QMessageBox.information(self, "Pogreška", "To slovo je pokusano i pogodeno") #Ne radi ako je slovo već pokusano!! i neradi na slovo r
            elif pokusajSlova in self.pokusana_slova:
                self.__porukaProzor("Pogreška", "To slovo je pokusano")


                QMessageBox.information(self, "Pogreška", "To slovo je pokusano") #Ne radi ako je slovo već pokusano!!
            elif pokusajSlova in self.pojamBezRazmaka:
                self.pogodena_slova.append(pokusajSlova)
                self.pokusana_slova.append(pokusajSlova)
                self.players[self.trenutniIgrac]['Bodovi'] += 1*self.vratiNagradu() #pygame nagrad
                self.prikaziStanje = self.funkcijaZaPrikazStanja(self.pojamSaRazmakom, self.pogodena_slova)
                self.trazenaRijecText.setText(self.prikaziStanje)

                if self.prikaziStanje == self.pojamSaRazmakom:
                    self.__porukaProzor(f"Čestitamo!\n{self.players[self.trenutniIgrac]['Username']} pogodio je zadnje slovo i riječ!\nZa izlaz klikni na 'x'")
                    '''QMessageBox.information(self, "Čestitamo!", f"{self.players[self.trenutniIgrac]['Username']} pogodio je zadnje slovo i riječ!")'''

            else:
                self.pokusana_slova.append(pokusajSlova)
                self.trenutniIgrac = (self.trenutniIgrac + 1) % len(self.players)
        else:  #Ako je pogoden pojam cijeli
            if pokusajSlova == self.pojamSaRazmakom:
                self.__porukaProzor(f"Čestitamo!\n{self.players[self.trenutniIgrac]['Username']} pogodio je riječ!\nZa izlaz klikni na 'x'")
                QMessageBox.information(self, "Čestitamo!", f"{self.players[self.trenutniIgrac]['Username']} pogodio je riječ!")

                self.players[self.trenutniIgrac]['Bodovi'] += 10*self.vratiNagradu 
                #pygame nagarad ili 500 Bodova za pogodenu cijelu rijec 
            else:
                self.trenutniIgrac = (self.trenutniIgrac + 1) % len(self.players)
                
        if(self.prikaziStanje == self.pojamSaRazmakom):
            self.show_results(self.players)
        
        self.unosSlovaText.setText("")
        self.igracNaReduText.setText(self.players[self.trenutniIgrac]["Username"])

    def funkcijaZaPrikazStanja(self, pojamSaRazmakom, pogodeni):
        displayed_word = ""
        for letter in pojamSaRazmakom:
            if letter ==" ":
                displayed_word += letter
            else:
                if letter in pogodeni:
                    displayed_word += letter
                else:
                    displayed_word += "_"
        return displayed_word
    
    def show_results(self, players):
        result_message = ""
        for player in players:
            result_message += f"{player['Username']}: {player['Bodovi']}\n"
        QMessageBox.information(self, "Bodovi:", f"{result_message}")


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



#SELECT poi.Naziv, Kat.Naziv as kategorija FROM Pojmovi poi INNER JOIN Kategorije Kat ON poi.idKategorija = Kat.id
#povezujemo pojmove s kategorijom
#as kategorija je da ne bi imali dva naziva,