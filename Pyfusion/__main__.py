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

from script_fusion.script_fusion_app import ScriptFusionApp


if __name__ == "__main__":
    app = ScriptFusionApp()
    app.mainloop()