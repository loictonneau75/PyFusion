import ttkbootstrap as ttk
import tkinter as tk
from tkinter import Frame, Misc, simpledialog, messagebox
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
        self.file_labelframe = ttk.LabelFrame(self, text = "liste des fichiers")

        #TODO : ajouter le fichier utils et main si ils n'existent pas encore
        self.file_name = ttk.Label(self.file_labelframe, text = "\n".join(key for key in self.classes.keys()))
        
        self.tree_view_repositery = ttk.Treeview(self, columns=("name", "path"))
        self.tree_view_repositery.heading("#0", text = "Structure")
        self.tree_view_repositery.heading("#1", text = "Nom du Dossier")
        self.tree_view_repositery.heading("#2", text = "chemin")
        self.tree_view_repositery.bind("<<TreeviewSelect>>", self.on_folder_select)
        self.root_folder = self.tree_view_repositery.insert("", tk.END, text = ".", values = (".", "./"))

        #TODO : a retirer
        self.essaie = self.add_folder("essaie",self.root_folder)

        self.button_fram = ttk.Frame(self)
        self.add_folder_button = ttk.Button(self.button_fram, text = "Ajouter", command = self.button_pressed_add_new_folder)
        self.delete_folder_button = ttk.Button(self.button_fram, text = "Supprimer", command = self.button_pressed_delete_selected_folder, state = tk.DISABLED)
        self.modify_folder_button = ttk.Button(self.button_fram,text = "Modifier", state = tk.DISABLED)
        self.place_widgets()

    def place_widgets(self) -> None:
        self.file_labelframe.grid(row = 0, column = 0)
        self.tree_view_repositery.grid(row = 0, column = 1)
        self.button_fram.grid(row = 0, rowspan = 2, column =3)
        self.add_folder_button.pack()
        self.delete_folder_button.pack()
        self.modify_folder_button.pack()
        self.file_name.pack()

    def add_folder(self, name, origin):
        if origin == self.root_folder:
            path = "./" + name
        else:
            parent_path = self.tree_view_repositery.item(origin)["values"][1]
            path = parent_path + "/" + name
        self.tree_view_repositery.insert(origin, tk.END, text=name, values=(name, path))

    def button_pressed_delete_selected_folder(self):
        selected_item = self.tree_view_repositery.selection()[0]
        if selected_item and selected_item != self.root_folder:
            self.tree_view_repositery.delete(selected_item)

    def button_pressed_add_new_folder(self):
        dialog = AddFolderDialog(self)
        if dialog.result:  
            new_folder_name, parent_folder_path = dialog.result
            print (f"parent folder path dans button pressed add new folder : {parent_folder_path}")
            if parent_folder_path == ".":
                parent_id = self.root_folder
            else:
                parent_id = self.find_parent_id(parent_folder_path)
            if not parent_id:  
                messagebox.showerror("Erreur", "Dossier parent non trouvé!")
                return
            self.add_folder(new_folder_name, origin=parent_id)

   
    def button_pressed_modify_selected_folder(self):
        pass 

    def on_folder_select(self, event: tk.Event):
        selected_item = self.tree_view_repositery.selection()
        if selected_item :
            self.modify_folder_button.config(state = tk.NORMAL)
            if selected_item[0] != self.root_folder:
                self.delete_folder_button.config(state = tk.NORMAL)
            else:
                self.delete_folder_button.config(state = tk.DISABLED)
        else:
            self.delete_folder_button.config(state = tk.DISABLED)
            self.modify_folder_button.config(state = tk.DISABLED)

    def get_all_folders(self, node = ''):
        folders = []
        for child in self.tree_view_repositery.get_children(node):
            item_values = self.tree_view_repositery.item(child)["values"]
            folder_path = item_values[1] if item_values else ""
            folders.append(folder_path)
            folders.extend(self.get_all_folders(child))
        return folders
    
    def find_parent_id(self, parent_name, node = ''):
        for child_id in self.tree_view_repositery.get_children(node):
            print(self.tree_view_repositery.item(child_id)["values"])
            if self.tree_view_repositery.item(child_id)["values"][1] == parent_name:
                return child_id
            result = self.find_parent_id(parent_name, child_id)
            if result:
                return result
        return None

class AddFolderDialog(simpledialog.Dialog):
    def body(self, parent: Frame) -> Misc | None:
        self.parent = parent
        self.create_widget()
        self.place_widget()

    def create_widget(self):
        self.folder_name_label = ttk.Label(self.parent, text = "Nom du dossier :")
        self.folder_name_entry = ttk.Entry(self.parent)
        self.parent_folder_choice_label = ttk.Label(self.parent, text = "Dossier parent :")
        self.existing_folders = self.master.get_all_folders()
        self.parent_folder_choice = ttk.Combobox(self.parent, values = self.existing_folders)

    def place_widget(self):
        self.folder_name_label.grid(row = 0, column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.folder_name_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.parent_folder_choice_label.grid(row = 1, column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.parent_folder_choice.grid(row = 1, column = 1, padx = 5, pady = 5)

    def buttonbox(self) -> None:
        box = Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        cancel_button = ttk.Button(box, text = "Cancel", width = 10, command = self.cancel,)
        cancel_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self) -> None:
        self.result = (self.folder_name_entry.get(), self.parent_folder_choice.get())
        
