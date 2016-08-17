# -*- coding: utf8 -*-
#VersesDownloader project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Module with Bible Functions"""
#pylint: disable=too-many-instance-attributes
#(i think 8 is reasonable in this case)

import urllib.request
import re

class Bible:
    """Interface for different bible translations."""

    shortcuts = {"Rdz": "Księga Rodzaju", "Wj": "Księga Wyjścia", "Kpł": "Księga Kapłańska",
                 "Lb": "Księga Liczb", "Pwt": "Księga Powtórzonego Prawa",
                 "Joz": "Księga Jozuego", "Sdz": "Księga Sędziów", "Rt": "Księga Rut",
                 "1 Sm": "1. Księga Samuela", "2 Sm": "2. Księga Samuela",
                 "1 Krl": "1. Księga Królewska", "2 Krl": "2. Księga Królewska",
                 "1 Krn": "1. Księga Kronik", "2 Krn": "2. Księga Kronik",
                 "Ezd": "Księga Ezdrasza", "Ne": "Księga Nehemiasza", "Tb": "Księga Tobiasza",
                 "Jdt": "Księga Judyty", "Est": "Księga Estery", "1 Mch": "1. Księga Machabejska",
                 "2 Mch": "2. Księga Machabejska", "Hi": "Księga Hioba", "Ps": "Księga Psalmów",
                 "Prz": "Księga Przysłów", "Koh": "Księga Koheleta (Księga Kaznodziei Salomona)",
                 "Pnp": "Pieśń nad pieśniami", "Mdr": "Księga Mądrości",
                 "Syr": "Mądrość Syracha", "Iz": "Księga Izajasza", "Jr": "Księga Jeremiasza",
                 "Lm": "Lamentacje Jeremiasza", "Ez": "Księga Ezechiela", "Dn": "Księga Daniela",
                 "Oz": "Księga Ozeasza", "Jl": "Księga Joela", "Am": "Księga Amosa",
                 "Ab": "Księga Abdiasza", "Jon": "Księga Jonasza", "Mi": "Księga Micheasza",
                 "Na": "Księga Nahuma", "Ha": "Księga Habakuka", "So": "Księga Sofoniasza",
                 "Ag": "Księga Aggeusza", "Za": "Księga Zachariasza", "Ml": "Księga Malachiasza",
                 "Mt": "Ewangelia św. Mateusza", "Mk": "Ewangelia św. Marka",
                 "Łk": "Ewangelia św. Łukasza", "J": "Ewangelia św. Jana",
                 "Dz": "Dzieje apostolskie", "Rz": "List do Rzymian",
                 "1 Kor": "1. List do Koryntian", "2 Kor": "2. List do Koryntian",
                 "Ga": "List do Galatów", "Ef": "List do Efezjan", "Flp": "List do Filipian",
                 "Kol": "List do Kolosan", "1 Tes": "1. List do Tesaloniczan",
                 "2 Tes": "2. List do Tesaloniczan", "1 Tm": "1. List do Tymoteusza",
                 "2 Tm": "2. List do Tymoteusza", "Tt": "List do Tytusa",
                 "Flm": "List do Filemona", "Hbr": "List do Hebrajczyków", "Jk": "List św. Jakuba",
                 "1 P": "1. List św. Piotra", "2 P": "2. List św. Piotra",
                 "1 J": "1. List św. Jana", "2 J": "2. List św. Jana", "3 J": "3. List św. Jana",
                 "Jud": "List św. Judy", "Ap": "Apokalipsa św. Jana"}

    def __init__(self, desc):
        self.desc = desc
        self._page = ""
        self._path = ""
        self._book = None
        self._chapter = None
        self._from = None
        self._to = None
        self.verses = []

    def __str__(self):
        result = self.desc + "\n"
        i = int(self._from) if self._from is not None else 1
        for verse in self.verses:
            result += "{0}: {1}\n".format(i, verse)
            i += 1
        return result

    def __len__(self):
        return len(self.verses)

    def __getitem__(self, index):
        return self.verses[index-1]

    def __iter__(self):
        for verse in self.verses:
            yield verse

    def diagnostic_print(self):
        """Print diagnostic information about object. For tests only."""
        res = ("Bible:\nDescription: {0}\nBook: {1}\nChapter: {2}\nFrom: {3}\nTo: {4}\n Path: {5}"
               .format(self.desc, self._book, self._chapter, self._from, self._to, self._path))
        print(res)

    def get_from(self):
        """Return starting verse index."""
        return int(self._from) if self._from is not None else 1

    def _download(self):
        """Download page with bible verses"""
        if self._path != "":
            self._page = urllib.request.urlopen(self._path).read().decode("utf-8")
        else:
            raise ValueError("Empty download path.")

    def _parse_desc(self):
        """Parse verses description"""
        #i feel like a hacker:
        #pylint: disable=line-too-long
        pattern = r"^\s*(?P<book>([0-3]\s)?[A-Za-z]+)\s+(?P<chapter>[0-9]+)\s*(,\s+(?P<from>[0-9]+)\s*-?\s*(?P<to>[0-9]+)?)?\s*$"
        parse_result = re.match(pattern, self.desc)
        if parse_result is None:
            raise ValueError("Parse error on book description.")
        self._book = parse_result.group("book")
        self._chapter = parse_result.group("chapter")
        self._from = parse_result.group("from")
        self._to = parse_result.group("to")

    def _build_path(self): #pylint: disable=no-self-use
        """Build web url to get actual verses"""
        raise AttributeError("Lack of building path function for this translation.")

    def _parse(self): #pylint: disable=no-self-use
        """Parse verses from page"""
        raise AttributeError("Lack of parse function for this bible translation.")

    def get(self):
        """Get Bible verses given by desc"""
        def to_index(attr):
            """Auxiliary function - from _to to index conversion"""
            return None if attr is None else int(attr)-1
        def from_index(attr):
            """Auxiliary function - from _from to index conversion"""
            return None if attr is None else int(attr)

        self._parse_desc()
        self._build_path()
        self._download()
        self._parse()
        self.verses = self.verses[to_index(self._from):from_index(self._to)]
        if not self.verses:
            raise ValueError("Given verses cannot be found.")
