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
import ttkbootstrap as ttk

from typing import Union

from utils import is_os_light_mode
from script_fusion.script_fusion_app import ScriptFusionApp
from class_separator.class_separator_app import ClassSeparator

class PyFusion(ttk.Window):
    def __init__(self):
        """
        Initialize the PyFusion app.

        Args:
            None

        Returns:
            None
        """
        theme = "flatly" if is_os_light_mode() else "darkly"
        super().__init__(themename=theme)
        self.title("Script Merger")
        self.resizable(False, False)

        self.create_widgets()


    def create_widgets(self):
        """
        Create GUI widgets for the application.

        Args:
            None

        Returns:
            None
        """
        self.merged_button = ttk.Button(self,text = "ScritpFusion", command = lambda: self.manage_button(ScriptFusionApp))
        self.separator_button = ttk.Button(self,text = "ClassSeparator", command = lambda: self.manage_button(ClassSeparator))
        
        self.place_widgets()

    def manage_button(self, app: Union[ScriptFusionApp, ClassSeparator]):
        self.destroy()
        app()

    def place_widgets(self):
        """
        Place widgets within the layout grid.

        Args:
            NoneApp

        Returns:
            None
        """
        self.merged_button.pack(padx=25, pady=(25, 7), fill='both')
        self.separator_button.pack(padx=25, pady=(7, 25), fill='both')


if __name__ == "__main__":
    app = PyFusion()
    app.mainloop()