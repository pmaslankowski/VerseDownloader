#NewInternationalVersion
#-*- coding: utf8 -*-
#Verse Downloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Module consists New International Version - implementations of Bible interface."""
import re
from bs4 import BeautifulSoup
from bible import Bible



class NewInternationalVersion(Bible):
    """NewInternationalVersion class."""

    books = {"Rdz": "Genesis", "Wj": "Exodus", "Kpł": "Levicitus", "Lb": "Numbers",
             "Pwt": "Deuteronomy", "Joz": "Joshua", "Sdz": "Judges", "Rt": "Ruth",
             "1 Sm": "1%20Samuel", "2 Sm": "2%20Samuel", "1 Krl": "1%20Kings",
             "2 Krl": "2%20Kings", "1 Krn": "1%20Chronicles", "2 Krn": "2%20Chronicles",
             "Ezd": "Ezra", "Ne": "Nehemiah", "Est": "Esther", "Hi": "Job", "Ps": "Psalm",
             "Prz": "Proverbs", "Koh": "Ecclesiastes", "Pnp": "Song%20of%20Songs",
             "Iz": "Isaiah", "Jr": "Jeremiah", "Lm": "Lamentations", "Ez": "Ezekiel",
             "Dn": "Daniel", "Oz": "Hosea", "Jl": "Joel", "Am": "Amos", "Ab": "Obadiah",
             "Jon": "Jonah", "Mi": "Micah", "Na": "Nahum", "Ha": "Habakkuk", "So": "Zephaniah",
             "Ag": "Haggai", "Za": "Zechariah", "Ml": "Malachi", "Mt": "Matthew", "Mk": "Mark",
             "Łk": "Luke", "J": "John", "Dz": "Acts", "Rz": "Romans", "1 Kor": "1%20Corinthians",
             "2 Kor": "2%20Corinthians", "Ga": "Galathians", "Ef": "Ephesians",
             "Flp": "Philippians", "Kol": "Colossians", "1 Tes": "1%20Thessalonians",
             "2 Tes": "2%20Thessalonians", "1 Tm": "1%20Timothy", "2 Tm": "2%20Timothy",
             "Tt": "Titus", "Flm": "Philemon", "Hbr": "Hebrews", "Jk": "James",
             "1 P": "1%20Peter", "2 P": "2%20Peter", "1 J": "1%20John", "2 J": "2%20John",
             "3 J": "3%20John", "Jud": "Jude", "Ap": "Revelation"}

    def __init__(self, desc):
        self.main_path = r"http://www.biblegateway.com"
        self.name = "New International Version"
        super().__init__(desc)

    def _build_path(self):
        book_name = NewInternationalVersion.books[self._book]
        self._path = ("{0}/passage/?search={1}+{2}&version=NIV"
                      .format(self.main_path, book_name, self._chapter))

    def _parse(self):
        ast = BeautifulSoup(self._page, "lxml")
        tmp = re.split("[0-9]+",
                       "".join([line.get_text() for line
                                in ast.find("div", class_="passage-text").findAll("p")]))
        #removing footnotes in [] and white characters:
        tmp = [re.sub(r"\[\w+\]", "", line).strip() for line in tmp]
        #removing empty lines:
        self.verses = tmp[1:-4]
        #removing copyright text:
        self.verses[-1] = self.verses[-1][:-56]
