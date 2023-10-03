import ttkbootstrap as ttk
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

        self.tree_view_repositery.heading(0, text="Nom du Dossier")
        self.tree_view_repositery.heading(1, text="Origine")
        
        # Ajout du dossier originel
        self.root_folder = self.tree_view_repositery.insert("", "end", text=".", values=("Dossier Originel", "."))
        
        self.place_widgets()

        # Exemple d'ajout de dossiers
        self.add_folder("Sous-Dossier1")
        # Pour ajouter d'autres dossiers, suivez le modèle ci-dessus.
    
    def place_widgets(self) -> None:
        self.file_labelframe.grid(row=0, column=0)
        self.tree_view_repositery.grid(row=0, column=1)
        self.class_name.pack()

    def add_folder(self, name, origin=None):
        """
        Ajoute un nouveau dossier à la Treeview
        :param name: Nom du nouveau dossier
        :param origin: ID du dossier parent (default est le dossier originel)
        """
        if origin is None:
            origin = self.root_folder
        self.tree_view_repositery.insert(origin, "end", text=name, values=(name, origin))

# À ce stade, vous pouvez continuer avec le reste de votre application, 
# comme la liaison d'événements, la gestion d'autres boutons ou widgets, etc.