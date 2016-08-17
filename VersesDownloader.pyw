# -*- coding: utf8 -*-
#VersesDownloader Project
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""Main program module - graphical version."""
import tkinter as Tk
import tkinter.ttk as Ttk
from tkinter import messagebox
import os
import re
import importlib
from time import strftime
from urllib import error as urlerror
import winsound
import pyperclip
import keyboard

#pylint: disable=too-many-instance-attributes
#pylint: disable=too-few-public-methods
class Application:
    """Main application class."""
    def __init__(self, master):
        self._translations = {} #dictionary with translation objects
        #names to ignore during searching translations:
        self._wrong_names = ["bible.py", "verses_downloader_text.py", "VersesDownloader.pyw"]
        self._selected_index = 1
        self._selected_verse = ""
        self._bible = None
        self._build_layout(master)
        self._load_translations()

    def _build_layout(self, master):
        master.minsize(width=500, height=600)
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

        self._verses_entry = Tk.Entry(input_frame, width="48", justify="center")
        self._verses_entry.grid(row=0, column=1, padx=(10, 0))
        self._verses_entry.focus_set()

        self._translation_combo = Ttk.Combobox(input_frame, state="readonly", width="45")
        self._translation_combo.grid(row=1, column=1, padx=(10, 0), pady=10)
        self._translation_combo["exportselection"] = False
        #remove focus after selecting item: (a bit tricky)
        self._translation_combo.bind("<FocusIn>", lambda event: event.widget.master.focus_set())

        Tk.Button(input_frame,
                  text="Pobierz",
                  command=self._download_verses,
                  padx=5).grid(row=2,
                               sticky="E",
                               column=1,
                               pady=(0, 15))
        master.bind("<Return>", self._download_verses)

        verses_frame.grid_columnconfigure(0, weight=1)
        up_arrow = Tk.PhotoImage(file="img/up-arrow.gif")
        self._up_button = Tk.Button(verses_frame, image=up_arrow, command=self._down_event)
        self._up_button.image = up_arrow
        self._up_button.grid(row=0, column=0, sticky="e")

        down_arrow = Tk.PhotoImage(file="img/down-arrow.gif")
        self._down_button = Tk.Button(verses_frame, image=down_arrow, command=self._up_event)
        self._down_button.image = down_arrow
        self._down_button.grid(row=0, column=1)

        self._verses_text = Tk.Text(verses_frame, state="disabled", width=48, wrap=Tk.WORD)
        self._verses_text.grid(row=1, column=0, columnspan=2, pady=5)

        self._verses_text.tag_configure("desc",
                                        font="Arial 9 italic")
        self._verses_text.tag_configure("index",
                                        font="Arial 6",
                                        lmargin1=10,
                                        spacing1=7)
        self._verses_text.tag_configure("verse",
                                        font="Arial 10",
                                        spacing1=7,
                                        lmargin2="20")
        self._verses_text.tag_configure("selected",
                                        font="Arial 10 underline",
                                        foreground="green")
        self._verses_text.tag_configure("source",
                                        font="Arial 9 italic",
                                        justify="right",
                                        rmargin=5)

    def _append_to_errors(self, msg): #pylint: disable=no-self-use
        with open("errorlog.txt", "a") as tmp:
            error = "{0}\n{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"), msg)
            tmp.write(error)

    def _load_translations(self):
        def get_name(fname):
            """Function gets object name from file.
               Object name is commented in first line of module file."""
            with open(fname, encoding="utf-8") as tmp:
                return tmp.readline()[1:].strip()

        pattern = r"^(?P<name>[A-Za-z_]+)\.py"
        translations = [fname for fname in os.listdir() if re.match(pattern, fname)]
        translations = list(set(translations) - set(self._wrong_names))
        labels = [] #values to show in combobox
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

    def _download_verses(self, event=None): #pylint: disable=W0613
        try:
            self._bible = self._translations[int(self._translation_combo.current())]
            self._bible.desc = self._verses_entry.get()
            self._bible.get()
            self._selected_index = self._bible.get_from()
            self._update_text()
            self._set_hotkeys()
            self._update_clipboard()
        except ValueError as error:
            messagebox.showerror("Błąd", str(error))
        except urlerror.URLError as error:
            messagebox.showerror("Błąd",
                                 "Wystąpił błąd przy łączeniu z serwerem.\n{0}".format(str(error)))
        finally:
            self._verses_text.configure(state="disabled")

    def _update_text(self):
        self._verses_text.configure(state="normal")
        self._verses_text.delete("1.0", "end")
        i = self._bible.get_from()
        self._verses_text.insert("end",
                                 "{0}: {1}\n".format(self._bible.name, self._bible.desc),
                                 "desc")
        for verse in self._bible:
            if i == self._selected_index:
                self._verses_text.insert("end", "{0} ".format(i), "index")
                self._verses_text.insert("end", "{0}\n".format(verse), "selected verse")
            else:
                self._verses_text.insert("end", "{0} ".format(i), "index")
                self._verses_text.insert("end", "{0}\n".format(verse), "verse")
            i += 1
        self._verses_text.insert("end", "źródło: {0}".format(self._bible.main_path), "source")
        self._verses_text.configure(state="disabled")

    def _set_hotkeys(self):
        keyboard.add_hotkey("ctrl+up", self._down_event)
        keyboard.add_hotkey("ctrl+down", self._up_event)

    def _clear_hotkeys(self): #pylint: disable=no-self-use
        keyboard.remove_hotkey("ctrl+up")
        keyboard.remove_hotkey("ctrl+down")

    def _up_event(self):
        if self._selected_index < len(self._bible) + self._bible.get_from() - 1:
            self._selected_index += 1
            self._update_clipboard()
            self._update_text()
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _down_event(self):
        if self._selected_index > self._bible.get_from():
            self._selected_index -= 1
            self._update_clipboard()
            self._update_text()
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _update_clipboard(self):
        pyperclip.copy(self._bible[self._selected_index-self._bible.get_from()+1])

if __name__ == "__main__":
    root = Tk.Tk() #pylint: disable=C0103
    app = Application(root) #pylint: disable=C0103
    root.mainloop()
