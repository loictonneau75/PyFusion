"""
Script Fusion App

This script provides a graphical user interface for merging Python script files
within a specified directory into a single output file.

The user can choose a target directory, and the script will scan the directory
for Python script files (with the ".py" extension), extract their import statements
and content, and merge them into a single output file named "merged_scripts.py" located in
a subdirectory named "merged_scripts".

Dependencies:
- os
- winreg
- tkinter
- filedialog from tkinter
- ttkbootstrap

Usage:
Run this script to launch the Script Fusion App. Choose a target directory
containing Python script files, and click the "Parcourir" button to select the
directory. After that, click the "Éxécuter" button to merge the script files and
create the output file.

Author: TONNEAU Loïc
"""
import tkinter as tk
import ttkbootstrap as ttk

from utils import is_os_light_mode
from script_fusion.script_fusion_app import ScriptFusionApp
from class_separator.class_separator_app import ClassSeparatorApp
from class_separator.TreeStructureApp import TreeStructureApp

class Main(ttk.Window):
    """
    Main Class for managing a tkinter application window.
    
    This class inherits from ttk.Window and sets up a GUI for merging Python scripts
    or separating Python classes. The user can choose between two functionalities
    via buttons: ScriptFusion and ClassSeparator. 

    Attributes:
        merged_button (ttk.Button): Button for ScriptFusion functionality.
        separator_button (ttk.Button): Button for ClassSeparator functionality.

    Methods:
        __init__(): Initialize the Main app with a specific theme.
        create_widgets(): Create GUI widgets for the application.
        manage_button(app: ScriptFusionApp | ClassSeparatorApp): Handle button behavior and switch apps.
        place_widgets(): Position the widgets within the layout pack.
    """
    def __init__(self):
        """
        Initialize the Main app.

        Args:
            None

        Returns:
            None
        """
        theme = "flatly" if is_os_light_mode() else "darkly"
        super().__init__(themename=theme)
        self.title("Script Merger")
        self.resizable(False, False)
        self.create_interface()

    def create_interface(self):
        self.app_frame = ttk.Frame(self)
        self.app_frame.grid(row = 0, column = 0)
        self.frame = AppChoiceApp(self.app_frame)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row = 1, column = 0)
        self.back_button = ttk.Button(self.button_frame, text = "Quit", command = self.destroy)
        self.back_button.pack()

    def go_to_new_app(self, app: ScriptFusionApp | ClassSeparatorApp | TreeStructureApp, dict: dict = None):
        """
        Manages the behavior of a button in the application. Destroys the current
        instance of the class and initializes a new instance of the specified application.

        Args:
            app (Union[ScriptFusionApp, ClassSeparatorApp]): The application class to initialize.

        Returns:
            None
        """
        self.frame.destroy()
        if app in (ScriptFusionApp,ClassSeparatorApp):
            self.frame = app(self.app_frame)
            self.back_button.config(text = "Return", command = self.return_to_app_choice)
        elif app == TreeStructureApp:
            self.frame = app(self.app_frame, dict)
            self.back_button.config(text = "Return", command = lambda: self.go_to_new_app(ClassSeparatorApp))

    def return_to_app_choice(self):
        """
        Returns to the AppChoiceApp frame from any other frame.

        Args:
            None

        Returns:
            None
        """
        self.frame.destroy()
        self.frame = AppChoiceApp(self.app_frame)
        self.back_button.config(text = "Quit", command = self.destroy)

class AppChoiceApp(ttk.Frame):
    def __init__(self, master: ttk.Window):
        self.master = master
        super().__init__(self.master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        """
        Create GUI widgets for the application.

        Args:
            None

        Returns:
            None
        """
        master = self.master.master
        self.merged_button = ttk.Button(self,text = "ScritpFusion", command = lambda: master.go_to_new_app(ScriptFusionApp))
        self.separator_button = ttk.Button(self,text = "ClassSeparator", command = lambda: master.go_to_new_app(ClassSeparatorApp))
        
        self.place_widgets()

    

    def place_widgets(self):
        """
        Place widgets within the layout pack.

        Args:
            NoneApp

        Returns:
            None
        """
        self.merged_button.pack(padx=25, pady=(25, 7), fill='both')
        self.separator_button.pack(padx=25, pady=(7, 25), fill='both')


if __name__ == "__main__":
    app = Main()
    app.mainloop()