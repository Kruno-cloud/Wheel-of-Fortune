class Pojam:
    def __init__(self,naziv:str, opis:str, idKategorije):
        self.naziv = naziv,
        self.idKategorija = idKategorije #Pojam mora imati svoju kategoriju
        self.opis = opis

    '''def pripremiZaJson(self):
        return {"ime":self.naziv,"opis":self.opis,"kategorija":self.kategorija}

    def __str__(self) -> str:
        return self.naziv+"\t"+self.kategorija+"\t"+self.opis+"\t"+str(self.kategorija)'''