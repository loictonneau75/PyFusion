import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog

from class_separator.class_separator import ClassSeparator

from utils import is_os_light_mode, from_class_name_to_str

class ClassSeparatorApp(ttk.Window):
    def __init__(self) -> None:
        theme = "flatly" if is_os_light_mode() else "darkly"
        super().__init__(themename = theme, title = from_class_name_to_str(self.__class__.__name__), resizable = (False, False))
        self.configure_grid()
        self.create_widgets()
        self.mainloop()

    def configure_grid(self) -> None:
        """
        Configure the layout grid for the application.

        Args:
            None

        Returns:
            None
        """
        self.columnconfigure(0, pad = 10)
        self.columnconfigure(1, pad = 10)

        self.rowconfigure(0, pad = 10)
        self.rowconfigure(1, pad = 10)
        self.rowconfigure(2, pad = 10)
        self.rowconfigure(3, pad = 10)
        self.rowconfigure(4, pad = 10)
        self.rowconfigure(5, pad = 10)

    def create_widgets(self) -> None:
        self.file_label = ttk.Label(self, text = "Choisissez le fichier cible :")
        self.file_entry = ttk.Entry(self)
        self.file_button = ttk.Button(self, text = "Parcourir", bootstyle = "secondary",
                                      command = lambda : self.file_entry.insert(tk.END, filedialog.askopenfilename()))
        self.folder_label = ttk.Label(self, text = "Choisissez le dossier cible :")
        self.folder_entry = ttk.Entry(self)
        self.folder_button = ttk.Button(self, text = "Parcourir", bootstyle = "secondary",
                                      command = lambda : self.folder_entry.insert(tk.END, filedialog.askdirectory()))
        self.execute_button = ttk.Button(self, text = "Éxécuter", bootstyle = "success",
                                         command = lambda: ClassSeparator(self.file_entry, self.folder_entry, self.result_label))
        self.result_label = ttk.Label(self, text = "")
        self.place_widgets()
    
    def place_widgets(self) -> None:
        self.file_label.grid(columnspan = 2, row = 0)
        self.file_entry.grid(column = 0, row = 1)
        self.file_button.grid(column = 1, row = 1)

        self.folder_label.grid(columnspan = 2, row = 2)
        self.folder_entry.grid(column = 0, row = 3)
        self.folder_button.grid(column = 1, row = 3)

        self.execute_button.grid(columnspan = 2, row = 4)
        self.result_label.grid(columnspan = 2, row = 5)