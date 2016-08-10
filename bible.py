# -*- coding: utf8 -*-
"""Module with Bible Functions"""
import urllib.request
import re

class Bible:
    """Interface for different bible translations."""
    def __init__(self):
        self.desc = ""
        self._page = ""
        self._path = ""
        self._book = None
        self._chapter = None
        self._from = None
        self._to = None
        self.verses = []

    def __str__(self):
        result = self.desc + "\n"
        i = int(self._from)
        for verse in self.verses:
            result += "{0}: {1}\n".format(i, verse)
            i += 1
        return result

    def diagnostic_print(self):
        result = ("Bible:\nDescription: {0}\nBook: {1}\nChapter: {2}\nFrom: {3}\nTo: {4}\n Path: {5}"
                  .format(self.desc, self._book, self._chapter, self._from, self._to, self._path))
        print(result)

    def _download(self):
        """Download page with bible verses"""
        if self._path != "":
            self._page = urllib.request.urlopen(self._path).read().decode("utf-8")
        else:
            raise ValueError("Empty download path.")

    def _parse_desc(self):
        """Parse verses description"""
        #i feel like a hacker:
        pattern = r"^\s*(?P<book>([0-3]\s)?[A-Za-z]+)\s+(?P<chapter>[0-9]+)\s*(,\s+(?P<from>[0-9]+)\s*-?\s*(?P<to>[0-9]+)?)?\s*$"
        parse_result = re.match(pattern, self.desc)
        if parse_result is None:
            raise ValueError("Parse error on book description.")
        self._book = parse_result.group("book")
        self._chapter = parse_result.group("chapter")
        self._from = parse_result.group("from")
        self._to = parse_result.group("to")
        if self._from is None:
            self._from = 1
        if self._to is None:
            self._to = int(self._from) + 1

    def _build_path(self):
        """Build web url to get actual verses"""
        raise AttributeError("Lack of building path function for this translation.")

    def _parse(self):
        """Parse verses from page"""
        raise AttributeError("Lack of parse function for this bible translation.")

    def get(self):
        """Get Bible verses given by desc"""
        self._parse_desc()
        self._build_path()
        self._download()
        self._parse()
        self.verses = self.verses[int(self._from):int(self._to)]


class BibliaWarszawska(Bible):
    """Biblia Warszawska - Brytyjka"""

    books_indexes = ["", "Rdz", "Wj", "Kpl", "Lb", "Pwt", "Joz", "Sdz", "Rt", "1 Sm",
                     "2 Sm", "1 Krl", "2 Krl", "1 Krn", "2 Krn", "Ezd", "Neh", "Est", "Hi",
                     "Ps", "Prz", "Koh", "Pnp", "Iz", "Jer", "Lm", "Ez", "Dn", "Oz",
                     "Jl", "Am", "Ab", "Jon", "Mi", "Na", "Ha", "So", "Ag", "Za", "Ml",
                     "Mt", "Mk", "Łk", "J", "Dz", "Rz", "1 Kor", "2 Kor", "Ga", "Ef",
                     "Flp", "Kol", "1 Tes", "2 Tes", "1 Tm", "2 Tm", "Tt", "Flm",
                     "Hbr", "Jk", "1 P", "2 P", "1 J", "2 J", "3 J", "Jud", "Ap"]

    def __init__(self):
        self.main_path = r"http://biblia-online.pl"
        self.name = "Biblia Warszawska"
        super().__init__()

    def _build_path(self):
        number = BibliaWarszawska.books_indexes.index(self._book)
        self._path = (self.main_path +
                      "/biblia,,,rozdzial,{0},wers,1,0,{1},1,t.html"
                      .format(self._chapter, number))

    def _parse(self):
        pattern = r'<td class="btxt".*?>(.*)?<br /></td>'
        self.verses = re.findall(pattern, self._page)

# b = BibliaWarszawska()
# b.desc = "1 Kor 13, 5"
# b.get()
# print(b)
