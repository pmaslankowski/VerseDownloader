# -*- coding: utf8 -*-
#VersesDownloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Main program module."""
import os
import re
import importlib

class VerseDownloader:
    """VerseDownloader main class."""
    def __init__(self):
        self._item = ""
        self._translations = [] #list with tuples: (module, class name)
        self.header = "=====================Narzędzie do pobierania wersetów======================="
        #names to ignore during searching translations:
        self._wrong_names = ["bible.py", "verse_downloader.py"]

    def run(self):
        """Running menu."""
        self._load_translations()
        self._start_screen()

    @staticmethod
    def _clear():
        os.system("cls")

    def _start_screen(self):
        #self._clear()
        print(self.header)
        print("Menu:")
        print("1. Pobieranie wersetów")
        print("2. Pomoc")
        print("3. Wyjście")
        option = input("Wybierz opcję:\n")
        if option == "1":
            self._item += "1"
            self._translations_screen()
        elif option == "2":
            self._item += "2"
        elif option == "3":
            self._item += "3"
        else:
            print("Wybrano błędną opcję. Wybierz 1, 2 lub 3.")

    def _load_translations(self):
        def get_name(fname):
            """Function gets object name from file.
               Object name is commented in first line of module file."""
            with open(fname, encoding="utf-8") as tmp:
                return tmp.readline()[1:].strip()

        pattern = r"^(?P<name>[A-Za-z_]+)\.py"
        translations = [fname for fname in os.listdir() if re.match(pattern, fname)]
        translations = list(set(translations) - set(self._wrong_names))
        for translation in translations:
            self._translations.append((importlib.import_module(translation[:-3]),
                                       get_name(translation)))

    def _translations_screen(self):
        self._clear()
        i = 1
        print(self.header)
        print("Dostępne wersje biblii:")
        for trans in self._translations:
            (module, classname) = trans
            tmp = getattr(module, classname)("")
            line = "{0}. {1} (źródło: {2})".format(i, tmp.name, tmp.main_path)
            print(line)
            i += 1
        print("\n")
        version = input("Wybierz właściwą opcję i naciśnij enter.\n")
