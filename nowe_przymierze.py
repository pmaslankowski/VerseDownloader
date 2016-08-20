#NowePrzymierze
#-*- coding: utf8 -*-
#Verse Downloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Module consists Nowe Przymierze translation - implementations of Bible interface."""
import re
from bs4 import BeautifulSoup
from bible import Bible



class NowePrzymierze(Bible):
    """NowePrzymierze - Tłumaczenie: Nowe Przymierze"""

    books = {"Mt": "Mateusz", "Mk": "Marek", "Łk": "Łukasz", "J": "Jan", "Dz": "Dzieje",
             "Rz": "Rzymian", "1 Kor": "1.%20Koryntian", "2 Kor": "2.%20Koryntian",
             "Ga": "Galacjan", "Ef": "Efezjan", "Flp": "Filipian", "Kol": "Kolosan",
             "1 Tes": "1.%20Tesaloniczan", "2 Tes": "2.%20Tesaloniczan", "1 Tm": "1.%20Tymoteusza",
             "2 Tm": "2.%20Tymoteusza", "Tt": "Tytusa", "Flm": "Filemona",
             "Hbr": "Hebrajczyk%C3%B3w", "Jk": "Jakuba", "1 P": "1.%20Piotra",
             "2 P": "2.%20Piotra", "1 J": "1.%20Jana", "2 J": "2.%20Jana",
             "3 J": "3.%20Jana", "Jud": "Judy", "Ap": "Objawienie"}

    def __init__(self, desc):
        self.main_path = r"http://www.biblegateway.com"
        self.name = "Nowe Przymierze"
        super().__init__(desc)

    def _build_path(self):
        book_name = NowePrzymierze.books[self._book]
        self._path = ("{0}/passage/?search={1}+{2}&version=NP"
                      .format(self.main_path, book_name, self._chapter))

    def _parse(self):
        ast = BeautifulSoup(self._page)
        tmp = re.split("[0-9]+",
                       "".join([line.get_text() for line
                                in ast.find("div", class_="passage-text").findAll("p")]))
        #removing footnotes in [] and white characters:
        tmp = [re.sub(r"\[\w+\]", "", line).strip() for line in tmp]
        #removing line "Copyright by Instytut Ewangeliczny":
        self.verses = tmp[1:-1]
        #removing copyright symbol:
        self.verses[-1] = self.verses[-1][:-2]
