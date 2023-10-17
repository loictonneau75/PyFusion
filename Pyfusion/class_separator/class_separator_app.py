import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog

from class_separator.class_separator import ClassSeparator
from utils import from_class_name_to_str

class ClassSeparatorApp(ttk.Labelframe):
    def __init__(self, master: ttk.Window, os) -> None: #TODO : retirer os
        self.master = master
        super().__init__(self.master, text = from_class_name_to_str(self.__class__.__name__))
        self.configure_grid()
        self.create_widgets(os)
        self.pack()

    def configure_grid(self) -> None:
        self.columnconfigure(0, pad = 10)
        self.columnconfigure(1, pad = 10)
        self.rowconfigure(0, pad = 10)
        self.rowconfigure(1, pad = 10)
        self.rowconfigure(2, pad = 10)
        self.rowconfigure(3, pad = 10)
        self.rowconfigure(4, pad = 10)
        self.rowconfigure(5, pad = 10)

    def create_widgets(self, os) -> None: #TODO : retirer os
        self.file_label = ttk.Label(self, text = "Choisissez le fichier cible :")
        self.file_entry = ttk.Entry(self)
        self.file_button = ttk.Button(self, text = "Parcourir", bootstyle = "secondary", command = self.search_file)
        self.folder_label = ttk.Label(self, text = "Choisissez le dossier cible :")
        self.folder_entry = ttk.Entry(self)
        self.folder_button = ttk.Button(self, text = "Parcourir", bootstyle = "secondary", command = self.search_directory )
        self.execute_button = ttk.Button(self, text = "Éxécuter", bootstyle = "success", command = self.managed_execute_button)
        self.result_label = ttk.Label(self, text = "")
        self.place_widgets()

        #TODO: remove
        if os == "Darwin":
            self.file_entry.insert(0, "/Users/loictonneau/Desktop/PyFusion/Pyfusion/merged_scripts/merged_scripts.py")
            self.folder_entry.insert(0, "/Users/loictonneau/Desktop/untitled folder")
        elif os == "Windows":
            self.file_entry.insert(0, "C:/Users/loict/Desktop/PyFusion/PyFusion/merged_scripts/merged_scripts.py")
            self.folder_entry.insert(0, "C:/Users/loict/Desktop/Nouveau dossier")
    
    def place_widgets(self) -> None:
        self.file_label.grid(columnspan = 2, row = 0)
        self.file_entry.grid(column = 0, row = 1)
        self.file_button.grid(column = 1, row = 1)
        self.folder_label.grid(columnspan = 2, row = 2)
        self.folder_entry.grid(column = 0, row = 3)
        self.folder_button.grid(column = 1, row = 3)
        self.execute_button.grid(columnspan = 2, row = 4)
        self.result_label.grid(columnspan = 2, row = 5)

    def managed_execute_button(self):
        ClassSeparator(self.master, self.file_entry, self.folder_entry, self.result_label)

    def search_directory(self):
        self.folder_entry.insert(tk.END, filedialog.askdirectory())

    def search_file(self):
        self.file_entry.insert(tk.END, filedialog.askopenfilename())