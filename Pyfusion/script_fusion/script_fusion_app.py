import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog


from utils import is_os_light_mode
from .script_fusion import ScriptFusion


class ScriptFusionApp(ttk.Window):
    """
    Main application class for the Script Fusion App.
    Contain the UI script.

    Attributes:
        None

    Methods:
        __init__(): Initializes the application.
        is_windows_light_mode(): Checks if Windows is in light mode.
        configure_grid(): Configures the layout grid.
        create_widgets(): Creates and places GUI widgets.
        place_widgets(): Places widgets within the grid.
    """
    def __init__(self):
        """
        Initialize the ScriptFusionApp.

        Args:
            None

        Returns:
            None
        """
        theme = "flatly" if is_os_light_mode() else "darkly"
        super().__init__(themename=theme)
        self.title("Script Merger")
        self.resizable(False, False)
        self.configure_grid()
        self.create_widgets()

    

    def configure_grid(self):
        """
        Configure the layout grid for the application.

        Args:
            None

        Returns:
            None
        """
        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)
        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)

    def create_widgets(self):
        """
        Create GUI widgets for the application.

        Args:
            None

        Returns:
            None
        """
        self.folder_label = ttk.Label(self, text="Choisissez le dossier cible :")
        self.folder_entry = ttk.Entry(self)
        self.folder_button = ttk.Button(self, text="Parcourir", bootstyle="secondary",
                                        command=lambda: self.folder_entry.insert(tk.END, filedialog.askdirectory()))
        self.execute_button = ttk.Button(self, text="Éxécuter", bootstyle="success",
                                         command=lambda: ScriptFusion (self.folder_entry, self.result_label))
        self.result_label = ttk.Label(self, text="")
        self.place_widgets()

    def place_widgets(self):
        """
        Place widgets within the layout grid.

        Args:
            NoneApp

        Returns:
            None
        """
        self.folder_label.grid(columnspan=2, row=0)
        self.folder_entry.grid(column=0, row=1)
        self.folder_button.grid(column=1, row=1)
        self.execute_button.grid(columnspan=2, row=2)
        self.result_label.grid(columnspan=2, row=3)
