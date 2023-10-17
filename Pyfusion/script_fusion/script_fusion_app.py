import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog

from script_fusion.script_fusion import ScriptFusion
from utils import from_class_name_to_str


class ScriptFusionApp(ttk.Labelframe):
    def __init__(self, master: ttk.Window, os) -> None:
        self.master = master
        self.os = os
        super().__init__(self.master, text = from_class_name_to_str(self.__class__.__name__))
        self.configure_grid()
        self.create_widgets()
        self.pack()

    def configure_grid(self) -> None:
        self.columnconfigure(0, pad = 10)
        self.columnconfigure(1, pad = 10)
        self.rowconfigure(0, pad = 10)
        self.rowconfigure(1, pad = 10)
        self.rowconfigure(2, pad = 10)

    def create_widgets(self) -> None:
        self.folder_label = ttk.Label(self, text = "Choisissez le dossier cible :")
        self.folder_entry = ttk.Entry(self)
        self.folder_button = ttk.Button(self, text = "Parcourir", bootstyle = "secondary", command = self.open_directory )
        self.execute_button = ttk.Button(self, text = "Éxécuter", bootstyle = "success", command = self.manage_execute )
        self.result_label = ttk.Label(self, text = "")
        self.place_widgets()

    def place_widgets(self) -> None:
        self.folder_label.grid(columnspan = 2, row = 0)
        self.folder_entry.grid(column = 0, row = 1)
        self.folder_button.grid(column = 1, row = 1)
        self.execute_button.grid(columnspan = 2, row = 2)
        self.result_label.grid(columnspan = 2, row = 3)

    def manage_execute(self):
        ScriptFusion (self.folder_entry, self.result_label, self.os)

    def open_directory(self):
        self.folder_entry.insert(tk.END, filedialog.askdirectory())

