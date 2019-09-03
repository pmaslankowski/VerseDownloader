#BibliaWarszawska
#-*- coding: utf8 -*-
#Verse Downloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Module consists Biblia Warszawska translation - implementations of Bible interface."""
import re
from bible import Bible
from bs4 import BeautifulSoup


class BibliaWarszawska(Bible):
    """Biblia Warszawska - Brytyjka"""

    books = {"Rdz": "1-Ksiega-Mojzeszowa",
			 "Wj": "2-Ksiega-Mojzeszowa", 
			 "Kpl": "3-Ksiega-Mojzeszowa",
			 "Lb": "4-Ksiega-Mojzeszowa",
			 "Pwt": "5-Ksiega-Mojzeszowa", 
			 "Joz": "Ksiega-Jozuego", 
			 "Sdz": "Ksiega-Sedziow",
			 "Rt": "Ksiega-Rut",
			 "1 Sm": "1-Ksiega-Samuela",
             "2 Sm": "2-Ksiega-Samuela",
             "1 Krl": "1-Ksiega-Krolewska",
             "2 Krl": "2-Ksiega-Krolewska", 
             "1 Krn": "1-Ksiega-Kronik",
             "2 Krn": "2-Ksiega-Kronik",
             "Ezd": "Ksiega-Ezdrasza", 
             "Neh": "Ksiega-Nehemiasza", 
             "Est": "Ksiega-Estery", 
             "Hi": "Ksiega-Joba",
             "Ps": "Ksiega-Psalmow", 
             "Prz": "Przypowiesci-Salomona", 
             "Koh": "Ksiega-Kaznodziei-Salomona", 
             "Pnp": "Piesn-nad-Piesniami", 
             "Iz": "Ksiega-Izajasza", 
             "Jer": "Ksiega-Jeremiasza", 
             "Lm": "Treny", 
             "Ez": "Ksiega-Ezechiela", 
             "Dn": "Ksiega-Daniela", 
             "Oz": "Ksiega-Ozeasza",
             "Jl": "Ksiega-Joela", 
             "Am": "Ksiega-Amosa", 
             "Ab": "Ksiega-Abdiasza", 
             "Jon": "Ksiega-Jonasza", 
             "Mi": "Ksiega-Micheasza", 
             "Na": "Ksiega-Nahuma", 
             "Ha": "Ksiega-Habakuka", 
             "So": "Ksiega-Sofoniasza", 
             "Ag": "Ksiega-Aggeusza", 
             "Za": "Ksiega-Zachariasza",
             "Ml": "Ksiega-Malachiasza",
             "Mt": "Ewangelia-Mateusza", 
             "Mk": "Ewangelia-Marka",
             "Łk": "Ewangelia-Lukasza", 
             "J": "Ewangelia-Jana", 
             "Dz": "Dzieje-Apostolskie", 
             "Rz": "List-do-Rzymian", 
             "1 Kor": "1-List-do-Koryntian",
             "2 Kor": "2-List-do-Koryntian", 
             "Ga": "List-do-Galacjan", 
             "Ef": "List-do-Efezjan",
             "Flp": "List-do-Filipian",
             "Kol": "List-do-Kolosan", 
             "1 Tes": "1-List-do-Tesaloniczan", 
             "2 Tes": "2-List-do-Tesaloniczan", 
             "1 Tm": "1-List-do-Tymoteusza", 
             "2 Tm": "2-List-do-Tymoteusza", 
             "Tt": "List-do-Tytusa", 
             "Flm": "List-do-Filemona",
             "Hbr": "List-do-Hebrajczykow",
             "Jk": "List-Jakuba",
             "1 P": "1-List-Piotra", 
             "2 P": "2-List-Piotra", 
             "1 J": "1-List-Jana", 
             "2 J": "2-List-Jana", 
             "3 J": "3-List-Jana", 
             "Jud": "List-Judy", 
             "Ap": "Objawienie-Swietego-Jana"}

    def __init__(self, desc):
        self.main_path = r"http://biblia-online.pl"
        self.name = "Biblia Warszawska"
        super().__init__(desc)

    def _build_path(self):
        book_name = BibliaWarszawska.books[self._book]
        self._path = (self.main_path +
                      "/Biblia/Warszawska/{0}/{1}/1/"
                      .format(book_name, self._chapter))

    def _parse(self):
        ast = BeautifulSoup(self._page, "lxml")
        self.verses = [tmp.getText() for tmp in ast.find_all("div", id=re.compile(r"vt[0-9]+"))]
