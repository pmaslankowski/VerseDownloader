# -*- coding: utf8 -*-
#VersesDownloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Main program module - text version."""
import os
import re
import importlib
import winsound

import keyboard
import pyperclip
from bible import Bible

#pylint: disable=too-many-instance-attributes
class VerseDownloader:
    """VerseDownloader main class."""
    def __init__(self):
        self.header = "=====================Narzędzie do pobierania wersetów======================="
        self._translations = [] #list with tuples: (module, class name)
        #names to ignore during searching translations:
        self._wrong_names = ["bible.py", "verses_downloader_text.py", "VersesDownloader.pyw"]
        self._errors = []
        self._selected = None #selected translation
        self._is_running = True
        self._action = self._start_screen #current screen
        self._selected_verse = None

    def run(self):
        """Running menu."""
        self._load_translations()
        while self._is_running:
            self._action()

    def exit(self):
        """Close program."""
        self._is_running = False

    @staticmethod
    def _clear():
        os.system("cls")

    def _print_errors(self):
        if self._errors:
            print("\n\nUwaga! Wystąpiły następujące błędy w trakcie działania programu:")
            i = 1
            for error in self._errors:
                print("{0}. {1}\n".format(i, error))
                i += 1

    def _start_screen(self):
        self._clear()
        print(self.header)
        print("Menu:")
        print("1. Pobieranie wersetów")
        print("2. Pomoc")
        print("3. Wyjście")
        self._print_errors()
        option = input("Wybierz opcję:\n")
        if option == "1":
            self._action = self._translations_screen
        elif option == "2":
            self._action = self._help_screen
        elif option == "3":
            self._action = self.exit
        else:
            input("Wybrano błędną opcję. Wybierz 1, 2 lub 3.")

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
            try:
                self._translations.append((importlib.import_module(translation[:-3]),
                                           get_name(translation)))
            except (SyntaxError, ImportError) as error:
                self._errors.append("Błąd w pliku: {0}\n{1}".format(translation,
                                                                    error))

    def _translations_screen(self):
        self._clear()
        i = 1
        translations = {} #dictionary with bible objects
        print(self.header)
        print("Dostępne wersje biblii:")
        for trans in self._translations:
            try:
                (module, classname) = trans
                tmp = getattr(module, classname)("")
                translations[i] = tmp
                line = "{0}. {1} (źródło: {2})".format(i, tmp.name, tmp.main_path)
            except AttributeError as error:
                line = "{0}. Błąd podczas wczytywania przekładu.".format(i)
                self._errors.append("Błąd podczas wczytywania przekładu" +
                                    " - błędna nazwa obiektu do utworzenia.\n{0}"
                                    .format(error))
            print(line)
            i += 1
        self._print_errors()
        version = input("Wybierz właściwą opcję i naciśnij enter.\n")
        try:
            self._selected = translations[int(version)]
            self._action = self._bible_screen
        except (KeyError, ValueError):
            input("Wybrano błędny przekład. Wciśnij enter aby wybierać ponownie.")

    def _bible_screen(self):
        self._clear()
        print(self.header)
        print("Wybrany przekład: {0}".format(self._selected.name))
        self._print_errors()
        self._selected.desc = input("Wprowadź wersety do pobrania: ")
        try:
            self._selected.get()
            self._action = self._verses_screen
        except ValueError as error:
            print("Wprowadzono błędny opis wersetów.\n{0}".format(error))
            self._action = self._bible_screen
            input()

    def _verses_screen(self):
        self._clear()
        print(self.header)
        print("Wybrany przekład: {0}".format(self._selected.name))
        print(self._selected)
        self._selected_verse = 1
        print("Zaznaczony werset: {0}".format(self._selected_verse))
        self._set_hotkeys()
        self._update_clipboard()
        self._print_errors()
        self._action = self._start_screen
        input("Naciśnij enter aby powrócić do głównego menu.\n")
        self._clear_hotkeys()

    def _help_screen(self):
        print("Zaznaczony werset: {0}".format(self._selected_verse))
        self._clear()
        print(self.header)
        print("Spis ksiąg biblijnych i ich skrótów używanych w programie:")
        for abbr, book in Bible.abbrs.items():
            print("{0} - {1}".format(abbr, book))
        self._print_errors()
        self._action = self._start_screen
        input("Naciśnij enter aby powrócić do głównego menu.")

    def _set_hotkeys(self):
        keyboard.add_hotkey("ctrl+up", self._up_event)
        keyboard.add_hotkey("ctrl+down", self._down_event)

    def _clear_hotkeys(self): #pylint: disable=no-self-use
        keyboard.remove_hotkey("ctrl+up")
        keyboard.remove_hotkey("ctrl+down")

    def _up_event(self):
        if self._selected_verse < len(self._selected):
            self._selected_verse += 1
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        self._update_clipboard()
        print("Zaznaczony werset: {0}".format(self._selected_verse))

    def _down_event(self):
        if self._selected_verse > 1:
            self._selected_verse -= 1
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        self._update_clipboard()
        print("Zaznaczony werset: {0}".format(self._selected_verse))

    def _update_clipboard(self):
        pyperclip.copy(self._selected[self._selected_verse])

if __name__ == "__main__":
    downloader = VerseDownloader() #pylint: disable=C0103
    downloader.run()
