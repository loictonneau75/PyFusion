import os
import winreg
import subprocess
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk


def get_files_and_path(directory: str, extension: str):
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
    return all(word not in input_string for word in word_list)

def get_text(path_list: list, file_list: list, output_file_name: str):
    existing_import = []
    main = []
    scripts = []
    for path in path_list:
        if not path.endswith(output_file_name):
            with open (path, "r") as file:
                    for line in file:
                        if line.startswith(("import","from")):
                            if line not in existing_import:
                                if check_words_in_string(file_list, line):
                                    existing_import.append(line)
                        else:
                            if path.endswith("main.py"):
                                main.append(line)
                            else:
                                scripts.append(line)
    scripts += main
    return existing_import, scripts

def create_test_file(file_path: str, imports: str, scripts: str):
    with open(file_path, "w") as output_file:
        output_file.writelines(imports)
        output_file.writelines(scripts)

def create_output_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def execute_script(folder_entry: ttk.Entry, result_label: ttk.Label):
    directory_path = folder_entry.get()

    if not directory_path:
        result_label.config(text = "Veuillez sélectionner un dossier")
        return
    
    if not os.path.exists(directory_path):
        result_label.config(text="Le chemin spécifié n'existe pas.")
        return
    
    subprocess.Popen(["explorer", directory_path])
    output_directory_name = "test"
    output_file_name = "test.py"

    create_output_directory(os.path.join(directory_path, output_directory_name))
    file_path = os.path.join(directory_path, output_directory_name, output_file_name)
    file_list, path_list = get_files_and_path(directory_path, ".py")
    imports, scripts = get_text(path_list, file_list, output_file_name)
    create_test_file(file_path, imports, scripts)

    result_label.config(text="Script exécuté avec succès !")

def is_windows_light_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return  apps_use_light_theme
    
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None

def main():
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
