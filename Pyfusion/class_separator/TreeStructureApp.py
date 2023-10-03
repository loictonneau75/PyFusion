import ttkbootstrap as ttk

from utils import from_class_name_to_str

class TreeStructureApp(ttk.Labelframe):
    def __init__(self, master: ttk.Window,) -> None:
        self.master = master
        super().__init__(self.master, text = from_class_name_to_str(self.__class__.__name__))
        ttk.Label(self, text = "TreeStructureApp").pack()
        self.pack()