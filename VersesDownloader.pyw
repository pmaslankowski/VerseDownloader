# -*- coding: utf8 -*-
# VersesDownloader Project
# Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""
Main program module - graphical version.
List of functions in this module:
   - __init__(self, master)
   - _build_layout(self, master)
   - _write_help(self)
   - _append_to_errors(self)
   - _load_translations(self)
   - _download_verses(self)
   - _update_text(self)
   - _set_hotkeys(self)
   - _clear_hotkeys(self)
   - _up_event(self)
   - _down_event(self)
   - _update_clipboard()
If this file is executed (not imported), it shows VersesDownloader main window.
"""

import tkinter as Tk
import tkinter.ttk as Ttk
from tkinter import messagebox
import os
import re
import importlib
import threading
from time import strftime
from urllib import error as urlerror
import bible
import winsound
import pyperclip
import keyboard


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class Application:
    """Main application class. """

    def __init__(self, master):
        """
        Function starts program, builds its layout and print help page.
        Function takes one argument: master - root of window widgets tree.
        """
        self._translations = {}  # dictionary with translation objects
        # names to ignore during searching translations:
        self._wrong_names = ["bible.py", "verses_downloader_text.py", "VersesDownloader.pyw"]
        self._selected_index = 1
        self._selected_verse = ""
        self._hotkeys_set = False
        self._lock = threading.Lock()
        self._status = Tk.StringVar()
        self._bible = None
        self._build_layout(master)
        self._load_translations()
        self._write_help()

    def _build_layout(self, master):
        """
        Function build main window layout.
        In second part, function defines tags in _verses_text.
        """
        master.minsize(width=650, height=600)
        master.wm_title("VersesDownloader")

        main_frame = Tk.Frame(master)
        main_frame.pack(padx=10, pady=10, expand=True, fill="both")

        input_frame = Tk.Frame(main_frame)
        input_frame.pack(expand=True, fill="both")

        verses_frame = Tk.Frame(main_frame)
        verses_frame.pack(expand=True, fill="both")

        master.grid_columnconfigure(1, weight=1)
        Tk.Label(input_frame, text="Wersety:").grid(row=0, sticky="W")
        Tk.Label(input_frame, text="Tłumaczenie:").grid(row=1, sticky="W", pady=10)

        self._verses_entry = Tk.Entry(input_frame, width="70", justify="center")
        self._verses_entry.grid(row=0, column=1, padx=(10, 0))
        self._verses_entry.focus_set()

        self._translation_combo = Ttk.Combobox(input_frame, state="readonly", width="67")
        self._translation_combo.grid(row=1, column=1, padx=(10, 0), pady=10)
        self._translation_combo["exportselection"] = False
        # remove focus after selecting item: (a bit tricky)
        self._translation_combo.bind("<FocusIn>", lambda event: event.widget.master.focus_set())

        Tk.Button(input_frame,
                  text="Cofnij",
                  command=self._write_help,
                  padx=5).grid(row=2,
                               sticky="W",
                               column=1,
                               pady=(0, 10))

        Tk.Button(input_frame,
                  text="Pobierz",
                  command=self._start_downloading,
                  padx=5).grid(row=2,
                               sticky="E",
                               column=1,
                               pady=(0, 10))
        master.bind("<Return>", self._start_downloading)

        verses_frame.grid_columnconfigure(0, weight=1)
        up_arrow = Tk.PhotoImage(file="img/up-arrow.gif")
        self._up_button = Tk.Button(verses_frame, image=up_arrow, command=self._up_event)
        self._up_button.image = up_arrow
        self._up_button.grid(row=0, column=0, pady=5, sticky="e")

        down_arrow = Tk.PhotoImage(file="img/down-arrow.gif")
        self._down_button = Tk.Button(verses_frame, image=down_arrow, command=self._down_event)
        self._down_button.image = down_arrow
        self._down_button.grid(row=0, column=1, pady=5)

        verses_frame2 = Tk.Frame(verses_frame)
        verses_frame2.grid(row=1, column=0, columnspan=2, rowspan=2)

        self._verses_header = Tk.Text(verses_frame2, state="disabled", width=66, height=2, wrap=Tk.WORD, borderwidth=0)
        self._verses_header.grid(row=0, column=0, columnspan=2, pady=0, sticky='s')

        self._verses_text_left = Tk.Text(verses_frame2, state="disabled", width=33, height=22, wrap=Tk.WORD, borderwidth=0)
        self._verses_text_left.grid(row=1, column=0, columnspan=1, pady=0)

        self._verses_text_right = Tk.Text(verses_frame2, state="disabled", width=33, height=22, wrap=Tk.WORD, borderwidth=0)
        self._verses_text_right.grid(row=1, column=1, columnspan=1, pady=0)


        self._verses_text_left.tag_configure("desc",
                                             font="Arial 9 italic")
        self._verses_text_left.tag_configure("index",
                                             font="Arial 6",
                                             lmargin1=10,
                                             spacing1=7)
        self._verses_text_left.tag_configure("verse",
                                             font="Arial 10",
                                             spacing1=7,
                                             lmargin2="20")
        self._verses_text_left.tag_configure("selected",
                                             font="Arial 10 bold",
                                             foreground="green")
        self._verses_text_left.tag_configure("source",
                                             font="Arial 9 italic",
                                             justify="right",
                                             rmargin=5)
        self._verses_text_left.tag_configure("help_abbr_old",
                                             font="Arial 10 bold",
                                             justify="left")
        self._verses_text_left.tag_configure("help_text_old",
                                             font="Arial 10",
                                             justify="left")
        self._verses_text_right.tag_configure("help_abbr_new",
                                              font="Arial 10 bold",
                                              justify="left")
        self._verses_text_right.tag_configure("help_text_new",
                                              font="Arial 10",
                                              justify="left")
        self._verses_header.tag_configure("help_header",
                                          font="Arial 14 bold",
                                          justify="center",
                                          spacing1=5,
                                          spacing3=10)

        self._status_bar = Tk.Label(master, textvariable=self._status, bd=1, relief=Tk.SUNKEN, anchor=Tk.W)
        self._status_bar.pack(side=Tk.BOTTOM, fill=Tk.X)

    def _write_help(self):
        """Function prints help in _verses_text"""

        def _fill(abbr_old, book_old, spaces):
            # removing polish characters to calculate proper length of strings:
            aux = {"ą": "a", "ę": "e", "ż": "z", "ź": "z", "ć": "c",
                   "ó": "o", "ń": "n", "ś": "s", "ł": "l"}
            for char, replacement in aux.items():
                abbr_old = abbr_old.replace(char, replacement)
                book_old = book_old.replace(char, replacement)
            return (spaces - len(abbr_old + " - " + book_old)) * " "

        self._status.set("Strona główna")
        self._verses_text_left.configure(state="normal", width=33, height=22)
        self._verses_text_left.delete("1.0", "end")

        self._verses_text_right.grid(row=1, column=1)
        self._verses_text_right.configure(state="normal")
        self._verses_text_right.delete("1.0", "end")

        self._verses_header.grid(row=0, column=0)
        self._verses_header.configure(state="normal")
        self._verses_header.delete("1.0", "end")
        self._verses_header.insert("end", "Spis ksiąg i skrótów", "help_header")

        for (abbr, book) in bible.Bible.old:
            self._verses_text_left.insert("end", f"{abbr}", "help_abbr_old")
            self._verses_text_left.insert("end", f" - {book}\n", "help_text_old")

        for (abbr, book) in bible.Bible.new:
            self._verses_text_right.insert("end", f"{abbr}", "help_abbr_new")
            self._verses_text_right.insert("end", f" - {book}\n", "help_text_new")

        self._verses_text_left.configure(state="disabled")
        self._verses_text_right.configure(state="disabled")
        self._verses_header.configure(state="disabled")

    def _append_to_errors(self, msg):  # pylint: disable=no-self-use
        """
        Function appends error to errorlog.txt
        msg is message to save.
        """
        with open("errorlog.txt", "a") as tmp:
            error = "{0}\n{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"), msg)
            tmp.write(error)

    def _load_translations(self):
        """
        Function loads available translations from program folder.
        Available translations are other .py files excluding _wrong_names in
        program directory.
        """

        def get_name(fname):
            """
            Function gets object name from file.
            Object name is commented in first line of module file.
            fname - name of file
            """
            with open(fname, encoding="utf-8") as tmp:
                return tmp.readline()[1:].strip()

        pattern = r"^(?P<name>[A-Za-z_]+)\.py"
        translations = [fname for fname in os.listdir() if re.match(pattern, fname)]
        translations = list(set(translations) - set(self._wrong_names))
        translations.sort()
        labels = []  # values to show in combobox
        i = 0
        for translation in translations:
            try:
                module = importlib.import_module(translation[:-3])
                classname = get_name(translation)
                obj = getattr(module, classname)("")
                self._translations[i] = obj
                labels.append("{0} (źródło: {1})".format(obj.name, obj.main_path))
                i += 1
            except (SyntaxError, ImportError) as error:
                self._append_to_errors("Błąd w pliku: {0}\n{1}".format(translation,
                                                                       error))
            except AttributeError as error:
                self._append_to_errors("Błąd podczas wczytywania przekładu" +
                                       " - błędna nazwa obiektu do utworzenia.\n{0}"
                                       .format(error))
        self._translation_combo["values"] = labels
        if len(labels) > 0:
            self._translation_combo.current(0)

    def _start_downloading(self, event=None):
        if self._lock.acquire(False):
            worker = threading.Thread(target=self._download_verses)
            worker.setDaemon(True)
            worker.start()
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _download_verses(self, event=None):  # pylint: disable=W0613
        """
        Function downloads selected verses, set hotkeys (ctrl + up, ctrl + down)
        and copy first verse to clipboard.
        Event argument is unused. It was added just to satisfy formal definition
        -this function is called when a download button is pressed.
        """
        try:
            self._bible = self._translations[int(self._translation_combo.current())]
            self._bible.desc = self._verses_entry.get().title()
            self._status.set("Pobieranie wersetów: {}...".format(self._bible.desc))
            self._bible.get()
            self._selected_index = self._bible.get_from()
            self._update_text()
            if not self._hotkeys_set:
                self._set_hotkeys()
            self._update_clipboard()
            self._status.set(self._bible.desc)
        except ValueError as error:
            messagebox.showerror("Błąd", str(error))
        except urlerror.URLError as error:
            messagebox.showerror("Błąd",
                                 "Wystąpił błąd przy łączeniu z serwerem.\n{0}".format(str(error)))
            self._status.set("")
        # except KeyError as error:
        #     messagebox.showerror("Błąd", "Nie znaleziono księgi: " + error.args[0])
        #     self._status.set("")
        finally:
            self._verses_text_left.configure(state="disabled")
            self._lock.release()

    def _update_text(self):
        """
        Function updates text in _verses_text.
        It removes whole old content and add new one (from _bible)
        """
        self._verses_text_left.configure(state="normal", width=66, height=24)
        self._verses_text_right.grid_remove()
        self._verses_header.grid_remove()
        self._verses_text_left.delete("1.0", "end")
        i = self._bible.get_from()
        self._verses_text_left.insert("end",
                                 "{0}: {1}\n".format(self._bible.name, self._bible.desc),
                                 "desc")
        for verse in self._bible:
            if i == self._selected_index:
                self._verses_text_left.insert("end", "{0} ".format(i), "index")
                self._verses_text_left.insert("end", "{0}\n".format(verse), "selected verse")
            else:
                self._verses_text_left.insert("end", "{0} ".format(i), "index")
                self._verses_text_left.insert("end", "{0}\n".format(verse), "verse")
            i += 1
        self._verses_text_left.insert("end", "źródło: {0}".format(self._bible.main_path), "source")
        self._verses_text_left.configure(state="disabled")

    def _set_hotkeys(self):
        """
        Function sets global hotkeys:
        -ctrl+up calls _up_event
        -ctrl+down calls _down_event
        """
        keyboard.add_hotkey("ctrl+up", self._up_event)
        keyboard.add_hotkey("ctrl+down", self._down_event)
        self._hotkeys_set = True

    def _clear_hotkeys(self):  # pylint: disable=no-self-use
        """Function disable hotkeys"""
        keyboard.remove_hotkey("ctrl+up")
        keyboard.remove_hotkey("ctrl+down")
        self._hotkeys_set = False

    def _down_event(self):
        """
        Function changes selected verse to upper one.
        If change is impossible, then info sound is played.
        """
        if self._selected_index < len(self._bible) + self._bible.get_from() - 1:
            self._selected_index += 1
            self._update_clipboard()
            self._update_text()
            self._verses_text_left.see(self._selected_index + 3.0)  # always show also 2 verses beneath
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _up_event(self):
        """
        Function changes selected verse to lower one.
        If change is impossible, then info sound is played.
        """
        if self._selected_index > self._bible.get_from():
            self._selected_index -= 1
            self._update_clipboard()
            self._update_text()
            self._verses_text_left.see(self._selected_index + 3.0)  # always show also 2 verses beneath
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _update_clipboard(self):
        """Function copy selected verse to clipboard"""
        pyperclip.copy(self._bible[self._selected_index - self._bible.get_from() + 1])


if __name__ == "__main__":
    root = Tk.Tk()  # pylint: disable=C0103
    app = Application(root)  # pylint: disable=C0103
    root.mainloop()
