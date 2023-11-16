from datetime import datetime
import re

class Igrac:
    id=0

    def __init__(self,ime:str,prezime:str,username:str, lozinka: str, datumRodenja:str, oib:str,drzavljanstvo:str,spol:str ): #Izbacimo sto ne zelimo
        self.ime = ime
        self.prezime = prezime
        try:
            self.datum_Rodenja=datetime.strptime(datumRodenja, "%d.%m.%Y") #datum_Rodenja je u formatu '01.01.2000' -> isto string

        except Exception:
            print("Datum rođenja se mora upisatu u formatu dan/mjesec/godina")
        if len(oib)!=11:
            raise Exception ("OIB MORA IMATI 11 ZNAMENKI!!")
        try:
            self.__oib = int(oib)
        except:
            raise Exception ("OIB SE SASTOJI SAMO OD ZNAMENKI!!")

        self.drzavljanstvo = drzavljanstvo
        self.spol = spol

        self.id = Igrac.id
        Igrac.id+=1
        self.username = username
        self._lozinka = None  # Initialize the _lozinka attribute
        # Call the setter method to validate and set the lozinka
        # the setter method for password is called implicitly when you set the password attribute using self.password = password within the constructor.
        self.lozinka = lozinka    
        

    #da se ne bi uneslo nesto sto nema 11 znakova
    def getOib(self):
        return self.__oib
    

    def setOib(self,oib):
        if len(oib)!=11:
            raise Exception ("OIB MORA IMATI 11 ZNAMENKI!!")
        try:
            self.__oib = int(oib)
        except:
            raise Exception ("OIB SE SASTOJI SAMO OD ZNAMENKI!!")


    @property #get self.lozinka
    def lozinka(self):
        return self._lozinka

    @lozinka.setter #set self.lozinka
    def lozinka(self, value):
        '''if self.is_valid_lozinka(value):
            self._lozinka = value
        else:
            raise ValueError("Invalid lozinka format")'''
        self._lozinka = value

    '''
    def is_valid_lozinka(self, lozinka):
        # Uz pomoc u re se porvjerava
        if (
            re.search(r'[A-Z]', lozinka) and # Sadrzi li lozinka velika slova od a - z
            re.search(r'[a-z]', lozinka) and # Sadrzi li lozinka mala slova
            re.search(r'[0-9]', lozinka) and # Sadrzi li lozinka brojeve od 0 do 9
            re.search(r'[!@#$%^&*]', lozinka) and # Sadrzi li lozinka specijalne znakove
            len(lozinka) >= 8 # Sadrzi li lozinka barem 8 ili vise znakova
        ): 
            return True #True se vraca u @lozinka.setter
        else:
            return False #False se vraca u @lozinka.setter
    '''    

    def pripremiZaJson(self):
        return {"Ime":self.ime,"Prezime":self.prezime,"Username":self.username, "Lozinka": self._lozinka,"Datum rodenja":str(self.datumRodenja.strftime("%Y-%m-%d")),"OIB":self.__oib,"Drzavljanstvo":self.drzavljanstvo, "Spol":self.spol}

    def __str__(self):
        return self.ime+"\t"+self.prezime+"\t\t"+ self.username + "\t\t"+str(self.datumRodenja)+"\t"+str(self.__oib)+"\t"+self.drzavljanstvo+"\t"+self.spol
