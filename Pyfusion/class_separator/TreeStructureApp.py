import ttkbootstrap as ttk
import tkinter as tk

from tkinter import Frame, Misc, simpledialog, messagebox

from class_separator.TreeStructure import TreeStructure
from utils import from_class_name_to_str

class TreeStructureApp(ttk.Frame):
    def __init__(self, master: ttk.Window, data: dict) -> None:
        self.master = master
        super().__init__(self.master, name = from_class_name_to_str(self.__class__.__name__))
        self.data = data
        self.classes : dict = self.data.get("classes", {})
        self.utils = self.data.get("utils", {})
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
        self._create_tree_view_repositery()
        self._create_file_arrangement_frame()
        self._create_button_frame()
        self.execute_button = ttk.Button(self, text = "Éxécuter", bootstyle = "success", command = lambda: TreeStructure(self.data, self.file_arrangement_dict_widget))
        self.place_widgets()
        self.update_comboboxes()

    def _create_tree_view_repositery(self):
        self.file_labelframe = ttk.LabelFrame(self, text = "liste des fichiers")
        self.file_list = self.create_file_list()
        self.tree_view_repositery = ttk.Treeview(self, columns = ("name", "path"), show = "tree headings")
        self.tree_view_repositery.heading("#0", text = "Structure")
        self.tree_view_repositery.heading("name", text = "Nom du Dossier")
        self.tree_view_repositery.heading("path", text = "chemin")
        self.tree_view_repositery.bind("<<TreeviewSelect>>", self.on_folder_select)
        self.root_folder = self.tree_view_repositery.insert("", tk.END, text = ".", values = (".", "."))
        self.expand_treeview()

    def expand_treeview(self, node=""):
        for child in self.tree_view_repositery.get_children(node):
            self.tree_view_repositery.item(child, open=True)
            self.expand_treeview(child) 

    def _create_file_arrangement_frame(self):
        self.file_arrangement_frame = ttk.Frame(self)
        self.file_arrangement_dict_name = {}
        for file in self.file_list:
            file_name = file + "_file"
            repo_name = file + "_repositery"
            self.file_arrangement_dict_name[file_name] = repo_name
            self.__setattr__(file_name, ttk.Label(self.file_arrangement_frame, text = file))
            self.__setattr__(repo_name, ttk.Combobox(self.file_arrangement_frame))

    def _create_button_frame(self):
        self.button_fram = ttk.Frame(self)
        self.add_folder_button = ttk.Button(self.button_fram, text = "Ajouter", command = self.button_pressed_add_new_folder)
        self.delete_folder_button = ttk.Button(self.button_fram, text = "Supprimer", command = self.button_pressed_delete_selected_folder, state = tk.DISABLED)
        self.modify_folder_button = ttk.Button(self.button_fram,text = "Modifier", command = self.button_pressed_modify_selected_folder, state = tk.DISABLED)

    def create_file_list(self):
        all_file_list = list(self.classes.keys())
        all_file_list.sort()
        if len(self.utils) > 0 and "utils" not in all_file_list:
            all_file_list.insert(0, "utils")
        if "main" not in all_file_list:
            all_file_list.insert(0, "main")
        else :
            all_file_list.remove("main")
            all_file_list.insert(0, "main")
        return all_file_list

    def update_comboboxes(self, new_combo=None):
        folder_names = self.get_all_folders()
        for combobox in [getattr(self, attr) for attr in self.file_arrangement_dict_name.values()]:
            combobox.set("choose folder")
            combobox["values"] = folder_names

    def place_widgets(self) -> None:
        self.tree_view_repositery.grid(row = 0, column = 0)
        self.button_fram.grid(row = 0, column = 1)
        self.file_arrangement_frame.grid(row = 1, columnspan = 2)
        self._place_widget_in_file_arrangement_frame()
        self._place_button_in_button_frame()
        self.execute_button.grid(columnspan = 2, row = 2)

    def _place_button_in_button_frame(self):
        self.add_folder_button.pack(fill = tk.X, pady = (0, 5))
        self.delete_folder_button.pack(fill = tk.X, pady = (0, 5))
        self.modify_folder_button.pack(fill = tk.X, pady = (0, 5))

    def _place_widget_in_file_arrangement_frame(self):
        i = 0
        j = 0
        self.from_name_to_widget()
        for label, combobox in self.file_arrangement_dict_widget.items():
            label.grid(row=i, column=0)
            combobox.grid(row=j, column=1)
            i += 1
            j += 1

    def from_name_to_widget(self):
        self.file_arrangement_dict_widget = {}
        for label_name, combobox_name in self.file_arrangement_dict_name.items():
            self.file_arrangement_dict_widget[getattr(self, label_name)] = getattr(self, combobox_name)
        return self.file_arrangement_dict_widget

    def add_folder(self, name: str, origin):
        if origin == self.root_folder:
            path = "./" + name
        else:
            parent_path = self.tree_view_repositery.item(origin)["values"][1]
            path = parent_path + "/" + name
        return self.tree_view_repositery.insert(origin, tk.END, text=name, values=(name, path))

    def button_pressed_delete_selected_folder(self):
        selected_item = self.tree_view_repositery.selection()[0]
        if selected_item and selected_item != self.root_folder:
            self.tree_view_repositery.delete(selected_item)
        self.update_comboboxes()
        self.expand_treeview()

    def button_pressed_add_new_folder(self):
        dialog = AddFolderDialog(self)
        if dialog.result:  
            new_folder_name, parent_folder_path = dialog.result
            if parent_folder_path == ".":
                parent_id = self.root_folder
            else:
                parent_id = self.find_parent_id(parent_folder_path)
            if not parent_id:  
                messagebox.showerror("Erreur", "Dossier parent non trouvé!")
                return
            self.add_folder(new_folder_name, origin = parent_id)
            self.update_comboboxes()
            self.expand_treeview()

    def button_pressed_modify_selected_folder(self):
        selected_item = self.tree_view_repositery.selection()[0]
        is_root_folder = True if selected_item == self.root_folder else False
        dialog = ModifyFolderDialog(self)
        if dialog.result:
            if is_root_folder :
                new_name = dialog.result
            else:
                new_name, new_parent_folder_path = dialog.result
                new_parent_folder = self.find_parent_id(new_parent_folder_path)
            if new_name != "":
                self.tree_view_repositery.item(selected_item, text = new_name, values = (new_name, self.tree_view_repositery.item(selected_item, "values")[1]))

            if new_parent_folder != "":
                if new_parent_folder == self.root_folder:
                    new_path = "./" + new_name
                else:
                    new_path = new_parent_folder_path + "/" + new_name
                self.tree_view_repositery.move(selected_item, new_parent_folder,tk.END)
                self.tree_view_repositery.item(selected_item, values = (self.tree_view_repositery.item(selected_item, "values")[0], new_path))
            self.update_comboboxes()
            self.expand_treeview()

    def on_folder_select(self, event: tk.Event):
        selected_item = self.tree_view_repositery.selection()[0]
        if selected_item :
            self.modify_folder_button.config(state = tk.NORMAL)
            if selected_item != self.root_folder:
                self.delete_folder_button.config(state = tk.NORMAL)
            else:
                self.delete_folder_button.config(state = tk.DISABLED)
        else:
            self.delete_folder_button.config(state = tk.DISABLED)
            self.modify_folder_button.config(state = tk.DISABLED)

    def get_all_folders(self, node='', exclude_node=None):
        folders = []
        if node == exclude_node:
            return []
        for child in self.tree_view_repositery.get_children(node):
            item_values = self.tree_view_repositery.item(child)["values"]
            folder_path = item_values[1] if item_values else ""
            if child != exclude_node:
                folders.append(folder_path)  
            folders.extend(self.get_all_folders(child, exclude_node=exclude_node))
        return folders

    def find_parent_id(self, parent_name, node = ''):
        for child_id in self.tree_view_repositery.get_children(node):
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
        existing_folders: list = self.master.get_all_folders()
        self.parent_folder_selected = tk.StringVar(self.parent)
        self.parent_folder_selected.set(existing_folders[0])
        self.parent_folder_selection = ttk.OptionMenu(self.parent, self.parent_folder_selected, existing_folders[0], *existing_folders)

    def place_widget(self):
        self.folder_name_label.grid(row = 0, column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.folder_name_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.parent_folder_choice_label.grid(row = 1, column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.parent_folder_selection.grid(row = 1, column = 1, padx = 5, pady = 5)

    def buttonbox(self) -> None:
        box = Frame(self)
        ok_button = ttk.Button(box, text="Validé", width=10, command=self.ok)
        ok_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        cancel_button = ttk.Button(box, text = "Annulé", width = 10, command = self.cancel,)
        cancel_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self) -> None:
        self.result = (self.folder_name_entry.get(), self.parent_folder_selected.get())


class ModifyFolderDialog(simpledialog.Dialog):
    def body(self, parent) -> Misc | None:
        self.parent = parent
        root_directory = self.master.root_folder
        self.tree_view_repositery = self.master.tree_view_repositery
        self.selected_item = self.tree_view_repositery.selection()[0]
        self.is_root_directory = self.selected_item == root_directory
        self.create_widget()
        self.place_widget()

    def create_widget(self):
        selected_item_path = self.tree_view_repositery.item(self.selected_item)["values"][1]
        self.actual_path_label = ttk.Label(self.parent, text = "chemin actuel :")
        self.actual_path = ttk.Label(self.parent, text = selected_item_path)
        self.new_name_label = ttk.Label(self.parent, text = "nouveau nom :")
        self.new_name_entry = ttk.Entry(self.parent)
        if not self.is_root_directory:
            self.new_parent_folder_label = ttk.Label(self.parent, text = "nouveau dossier parent")
            existing_folders = self.master.get_all_folders(exclude_node = self.selected_item)
            self.new_parent_folder_entry = ttk.Combobox(self.parent, values = existing_folders)

    def place_widget(self):
        self.actual_path_label.grid(column = 0, row = 0, sticky = tk.E, padx = 5, pady = 5)
        self.actual_path.grid(column = 1, row = 0,sticky = tk.W, padx = 5, pady = 5)
        self.new_name_label.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)
        self.new_name_entry.grid(column = 1, row = 1, padx = 5, pady = 5)
        if not self.is_root_directory:
            self.new_parent_folder_label.grid(column = 0, row = 2, sticky = tk.W, padx = 5, pady = 5)
            self.new_parent_folder_entry.grid(column = 1, row = 2, padx = 5, pady = 5)

    def buttonbox(self) -> None:
        box = Frame(self)
        ok_button = ttk.Button(box, text="Validé", width=10, command=self.ok)
        ok_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        cancel_button = ttk.Button(box, text = "Annulé", width = 10, command = self.cancel,)
        cancel_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self):
        if self.is_root_directory:
            self.result = self.new_name_entry.get()
        else :
            self.result = (self.new_name_entry.get(), self.new_parent_folder_entry.get())
