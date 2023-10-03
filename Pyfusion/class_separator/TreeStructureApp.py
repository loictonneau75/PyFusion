import ttkbootstrap as ttk
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import from_class_name_to_str

class TreeStructureApp(ttk.Labelframe):
    def __init__(self, master: ttk.Window, data: dict) -> None:
        self.master = master
        super().__init__(self.master, text=from_class_name_to_str(self.__class__.__name__))
        self.classes = data.get("classes", {})
        self.utils = data.get("utils", None)
        self.configure_grid()
        self.create_widgets()
        self.pack()

    def configure_grid(self) -> None:
        pass

    def create_widgets(self) -> None:
        self.file_labelframe = ttk.LabelFrame(self, text="liste des fichiers")
        self.class_name = ttk.Label(self.file_labelframe, text="\n".join(key for key in self.classes.keys()))
        
        # Initialisation du Treeview
        self.tree_view_repositery = ttk.Treeview(self, columns=("name", "origin"))
        self.tree_view_repositery.heading("#0", text="Structure")
        self.tree_view_repositery.heading("#1", text="Nom du Dossier")
        self.tree_view_repositery.heading("#2", text="Origine")
        
        # Ajout du dossier originel
        self.root_folder = self.add_folder(".","")

        self.button_fram = ttk.Frame(self)
        self.add_folder_button = ttk.Button(self.button_fram, text="Ajouter")
        self.delete_folder_button = ttk.Button(self.button_fram, text="Supprimer", command=self.delete_selected_folder, state=tk.DISABLED)  # initialement désactivé
        self.modify_folder_button = ttk.Button(self.button_fram,text = "Modifier", state = tk.DISABLED)

        self.place_widgets()

    def place_widgets(self) -> None:
        self.file_labelframe.grid(row=0, column=0)
        self.tree_view_repositery.grid(row=0, column=1)
        self.button_fram.grid(row = 0, rowspan = 2, column =3)
        self.add_folder_button.pack()
        self.delete_folder_button.pack()
        self.modify_folder_button.pack()
        self.class_name.pack()

    def add_folder(self, name, origin):
        self.tree_view_repositery.insert(origin, "end", text=name, values=(name, origin))

    def delete_selected_folder(self):
        selected_item = self.tree_view_repositery.selection()[0]  # obtient l'ID de l'élément sélectionné
        if selected_item and selected_item != self.root_folder:  # vérifie si un élément est sélectionné et qu'il ne s'agit pas du dossier racine
            self.tree_view_repositery.delete(selected_item)
   