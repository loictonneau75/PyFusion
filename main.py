import os
import winreg
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk


def is_windows_light_mode():
    """
    Check if the Windows operating system is using light mode.

    Returns:
        bool: True if Windows is in light mode, False otherwise.
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return  apps_use_light_theme
    
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None

def create_output_directory(path: str):
    """
    Create an output directory if it doesn't exist.

    Args:
        path (str): The path of the directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def get_files_and_path(directory: str, extension: str):
    """
    Get a list of files and their paths with a specific extension within a directory.

    Args:
        directory (str): The target directory to search for files.
        extension (str): The file extension to filter.

    Returns:
        Tuple[list, list]: A tuple containing two lists - file_list and path_list.
            file_list: List of file names (without extension).
            path_list: List of corresponding file paths.
    """
    file_list = []
    path_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_name, _ = os.path.splitext(file)
                file_list.append(file_name)
                path_list.append(os.path.join(root, file))

    return file_list, path_list

def check_words_in_string(word_list: list, input_string: str):
    """
    Check if any of the words in a list are present in the input string.

    Args:
        word_list (list): List of words to check.
        input_string (str): The input string to search in.

    Returns:
        bool: True if none of the words are found, False otherwise.
    """
    return all(word not in input_string for word in word_list)

def process_import(line: str, existing_import: list, file_list: list):
    """
    Process an import line and update the existing import list.

    Args:
        line (str): The import line to process.
        existing_import (list): List of existing import lines.
        file_list (list): List of file names to check against.
    """
    if line.startswith(("import","from")):
        if line not in existing_import:
            if check_words_in_string(file_list, line):
                existing_import.append(line)

def process_content(line: str, path: str, main: list, scripts: list):
    """
    Categorize a line of code into the main section or the scripts section.

    Args:
        line (str): The line of code to categorize.
        path (str): The path of the file being processed.
        main (list): List to store lines for the main section.
        scripts (list): List to store lines for the scripts section.
    """
    if not line.startswith(("import","from")):
        if path.endswith("main.py"):
            main.append(line)
        else:
            scripts.append(line)

def get_text(path_list: list, file_list: list, output_file_name: str):
    """
    Process the content of input files and separate imports from scripts.

    Args:
        path_list (list): List of file paths to process.
        file_list (list): List of file names to check against.
        output_file_name (str): Name of the output file.

    Returns:
        Tuple[list, list]: A tuple containing two lists - existing_import and scripts.
            existing_import: List of existing import lines.
            scripts: List of lines for the merged script.
    """
    existing_import = []
    main = []
    scripts = []
    for path in path_list:
        if not path.endswith(output_file_name):
            with open (path, "r") as file:
                for line in file:
                    process_import(line, existing_import, file_list)
                    process_content(line, path, main, scripts)
    scripts += main
    return existing_import, scripts

def create_merged_file(file_path: str, imports: str, scripts: str):
    """
    Create a merged output file with imports and scripts.

    Args:
        file_path (str): Path of the output file to create.
        imports (str): Import lines to write into the output file.
        scripts (str): Script lines to write into the output file.
    """
    with open(file_path, "w") as output_file:
        output_file.writelines(imports)
        output_file.writelines(scripts)

def execute_script(folder_entry: ttk.Entry, result_label: ttk.Label):
    """
    Execute the script merging process based on user input.

    Args:
        folder_entry (ttk.Entry): GUI entry widget for folder selection.
        result_label (ttk.Label): GUI label widget to display results.
    """
    directory_path = folder_entry.get()
    if not directory_path:
        result_label.config(text = "Veuillez sélectionner un dossier")
        return
    if not os.path.exists(directory_path):
        result_label.config(text="Le chemin spécifié n'existe pas.")
        return
    
    output_directory_name = "test"
    output_file_name = "test.py"

    output_directory_path = os.path.join(directory_path, output_directory_name)
    create_output_directory(output_directory_path)
    
    file_path = os.path.join(output_directory_path, output_file_name)
    file_list, path_list = get_files_and_path(directory_path, ".py")
    imports, scripts = get_text(path_list, file_list, output_file_name)
    create_merged_file(file_path, imports, scripts)

    result_label.config(text="Script exécuté avec succès !")
    os.system(f'explorer "{os.path.abspath(output_directory_path)}"')

def main():
    """
    Entry point of the script. Initializes the GUI and executes the script merging process.

    This function sets up the graphical user interface (GUI) using the `tkinter` library.
    It creates labels, entry fields, buttons, and configures their layout.
    The 'Exécuter' button triggers the script merging process using the `execute_script()` function.
    
    Note:
        This function relies on other functions and elements defined in the script.

    Returns:
        None
    """
    theme = "flatly" if is_windows_light_mode() else "darkly"
    root = ttk.Window(themename = theme)
    root.title("Script Merger")
    root.resizable(False, False)

    folder_label = ttk.Label(root, text="Choisissez le dossier cible:")
    folder_entry = ttk.Entry(root)
    folder_button = ttk.Button(root, text="Parcourir", bootstyle = "secondary", 
                               command=lambda: folder_entry.insert(tk.END, filedialog.askdirectory()))
    execute_button = ttk.Button(root, text="Exécuter", bootstyle = "success", 
                                command = lambda: execute_script(folder_entry,result_label))
    result_label = ttk.Label(root, text="")

    root.columnconfigure(0, pad = 10)
    root.columnconfigure(1, pad = 10)
    root.rowconfigure(0, pad = 10)
    root.rowconfigure(1, pad = 10)
    root.rowconfigure(2, pad = 10)

    folder_label.grid(columnspan = 2, row = 0)
    folder_entry.grid(column = 0, row = 1)
    folder_button.grid(column = 1, row = 1)
    execute_button.grid(columnspan = 2, row = 2)
    result_label.grid(columnspan = 2, row = 3)

    root.mainloop()

if __name__ == "__main__":
    main()
