#BibliaWarszawska
#-*- coding: utf8 -*-
#Verse Downloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Module consists Biblia Warszawska translation - implementations of Bible interface.c"""
import re
from bible import Bible


class BibliaWarszawska(Bible):
    """Biblia Warszawska - Brytyjka"""

    books_indexes = ["", "Rdz", "Wj", "Kpl", "Lb", "Pwt", "Joz", "Sdz", "Rt", "1 Sm",
                     "2 Sm", "1 Krl", "2 Krl", "1 Krn", "2 Krn", "Ezd", "Neh", "Est", "Hi",
                     "Ps", "Prz", "Koh", "Pnp", "Iz", "Jer", "Lm", "Ez", "Dn", "Oz",
                     "Jl", "Am", "Ab", "Jon", "Mi", "Na", "Ha", "So", "Ag", "Za", "Ml",
                     "Mt", "Mk", "Łk", "J", "Dz", "Rz", "1 Kor", "2 Kor", "Ga", "Ef",
                     "Flp", "Kol", "1 Tes", "2 Tes", "1 Tm", "2 Tm", "Tt", "Flm",
                     "Hbr", "Jk", "1 P", "2 P", "1 J", "2 J", "3 J", "Jud", "Ap"]

    def __init__(self, desc):
        self.main_path = r"http://biblia-online.pl"
        self.name = "Biblia Warszawska"
        super().__init__(desc)

    def _build_path(self):
        number = BibliaWarszawska.books_indexes.index(self._book)
        self._path = (self.main_path +
                      "/biblia,,,rozdzial,{0},wers,1,0,{1},1,t.html"
                      .format(self._chapter, number))

    def _parse(self):
        pattern = r'<td class="btxt".*?>(.*)?<br /></td>'
        self.verses = re.findall(pattern, self._page)
