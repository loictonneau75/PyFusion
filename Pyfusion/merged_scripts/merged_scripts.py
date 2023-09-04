import winreg
import os
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog


def is_os_light_mode():
        """
        Check if os is in light mode.

        Args:
            None

        Returns:
            bool: True if Windows is in light mode, False otherwise.
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            is_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return is_light_theme
        except Exception as e:
            print("Erreur lors de la détection du thème:", e)
            return None
        





class ScriptFusion ():
    """
    ScriptFusion  class for merging Python script files.

    Attributes:
        extension (str): The file extension to look for.
        target_directory (str): The target directory for script files.
        output_directory_name (str): Name of the output directory.
        output_directory_path (str): Path of the output directory.
        output_file_name (str): Name of the output merged file.
        output_file_path (str): Path of the output merged file.
        file_list (list): List of Python script file names (without extension).
        path_list (list): List of paths to Python script files.
        import_statements (list): List of import statements.

    Methods:
        __init__(folder_entry: ttk.Entry, result_label: ttk.Label): Initialize the ScriptFusion .
        create_output_directory(): Create the output directory if it doesn't exist.
        find_python_files_in_directory(): Find Python script files in the target directory.
        check_words_in_string(line: str): Check if any word from file_list is present in the line.
        process_import_statement(line: str): Process import statements in the line.
        process_script_content(line, path): Process script content based on the line and path.
        process_content(): Process the content of script files.
        merge_script_files(): Merge the script files into the output file.
        start_script_merger(): Start the script merging process.
        get_result(result_label: ttk.Label): Update the result label with the execution status.
    """
    def __init__(self, folder_entry: ttk.Entry, result_label: ttk.Label):
        """
        Initialize the ScriptFusion .

        Args:
            folder_entry (ttk.Entry): Entry widget containing the target directory.
            result_label (ttk.Label): Label widget to display execution results.

        Returns:
            None
        """
        self.target_directory = folder_entry.get()
        self.result_label = result_label
        if self.check_input():
            self.extension = ".py"
            self.file_list = []
            self.path_list = []
            self.start_script_merger()
            self.get_result(result_label)

    def check_input(self) -> bool:
        if not self.target_directory:
            self.result_label.config(text = "Veuillez inscrire un dossier !")
            return False
        if not os.path.exists(self.target_directory):
            self.result_label.config(text = "Le chemin spécifié n'existe pas !")
            return False
        return True

    def create_output_directory(self):
        """
        Create the output directory if it doesn't exist.

        Args:
            None

        Returns:
            None
        """
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

    def find_python_files_in_directory(self):
        """
        Find Python script files in the target directory.

        Args:
            None

        Returns:
            None
        """
        for root, _, files in os.walk(self.target_directory):
            for file in files:
                if file.endswith(self.extension):
                    file_name, _ = os.path.splitext(file)
                    self.file_list.append(file_name)
                    self.path_list.append(os.path.join(root, file))

    def check_words_in_string(self, line: str):
        """
        Check if any word from file_list is present in the line.

        Args:
            line (str): Line of text to check.

        Returns:
            bool: True if none of the words in file_list are present, False otherwise.
        """
        return all(word not in line for word in self.file_list)
    
    def process_comment_statement(self):
        """
        Process comment before the script.
        
        Args:
            None
            
        Returns:
            None
        """
        #TODO: récuperer le commentaire de presnetation de l'appli et le metter en haut du fichier fusioné
        pass

    def process_import_statement(self, line: str):
        """
        Process import statements in the line.

        Args:
            line (str): Line of text to process.

        Returns:
            None
        """
        if line.startswith(("import","from")):
            if line not in self.import_statements and self.check_words_in_string(line):
                self.import_statements.append(line)

    def process_script_content(self, line, path):
        """
        Process script content based on the line and path.

        Args:
            line (str): Line of text to process.
            path (str): Path to the script file containing the line.

        Returns:
            None
        """
        if not line.startswith(("import", "from")):
            if path.endswith("main.py"):
                self.main_file_content.append(line)
            else:
                self.script_content.append(line)

    def process_content(self):
        """
        Process the content of script files.

        Args:
            None

        Returns:
            None
        """
        self.import_statements = []
        self.main_file_content = []
        self.script_content = []
        for path in self.path_list:
            if not path.endswith(self.output_file_name):
                with open(path, "r") as file:
                    for line in file:
                        self.process_import_statement(line)
                        self.process_script_content(line, path)
        self.script_content += self.main_file_content

    def merge_script_files(self):
        """
        Merge the script files into the output file.

        Args:
            None

        Returns:
            None
        """
        with open(self.output_file_path,"w") as output_file:
            output_file.writelines(self.import_statements)
            output_file.writelines(self.script_content)

    def start_script_merger(self):
        """
        Start the script merging process.

        Args:
            None

        Returns:
            None
        """
        self.output_directory_name = "merged_scripts"
        self.output_directory_path = os.path.join(self.target_directory, self.output_directory_name)
        self.create_output_directory()

        self.output_file_name = "merged_scripts.py"
        self.output_file_path = os.path.join(self.output_directory_path,self.output_file_name)

        self.find_python_files_in_directory()
        self.process_content()
        self.merge_script_files()

    def get_result(self, result_label: ttk.Label):
        """
        Update the result label with the execution status.

        Args:
            result_label (ttk.Label): Label widget to display execution results.

        Returns:
            None
        """
        result_label.config(text = "Script exécuté avec succès !")
        os.system(f'explorer "{os.path.abspath(self.output_directory_path)}"')




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


if __name__ == "__main__":
    app = ScriptFusionApp()
    app.mainloop()