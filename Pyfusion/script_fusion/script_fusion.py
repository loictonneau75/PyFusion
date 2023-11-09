import os
import ttkbootstrap as ttk


class ScriptFusion ():
    def __init__(self, folder_entry: ttk.Entry, result_label: ttk.Label, os , extension = ".py") -> None:
        #TODO : rendre possible le script avec d'autre language doinc en changeant l'extension
        self.root_directory = folder_entry.get()
        self.target_directory = self.find_script_directory()
        self.label = result_label
        self.os = os
        self.extension = extension
        if self.check_input():
            self.files_in_directory = []
            self.path_files_in_directory = []
            self.initialize_directories_and_files()

            self.presentation = []
            self.imports = []
            self.main_file_content = []
            self.other_files_content = []
            self.script_merger()
            
            self.show_result()

    def find_script_directory(self) -> str:
        target_base_name = os.path.basename(self.root_directory)
        for root, dirs, _ in os.walk(self.root_directory):
            if target_base_name in dirs:
                return os.path.join(root, target_base_name)
        return self.root_directory

    def check_input(self) -> bool:
        if not self.target_directory:
            self.label.config(text = "Veuillez inscrire un dossier !")
            return False
        if not os.path.exists(self.target_directory):
            self.label.config(text = "Le chemin spécifié n'existe pas !")
            return False
        return  True

    def initialize_directories_and_files(self) -> None:
        self.output_directory_name = "merged_scripts"
        self.output_file_name = "merged_scripts.py"
        self.output_directory_path = os.path.join(self.target_directory, self.output_directory_name)
        self.output_file_path = os.path.join(self.output_directory_path,self.output_file_name)

    def add_ligne_gitignore(self) -> None:
        gitignore_path = os.path.join(self.root_directory, '.gitignore')
        ignore_line = f'{self.output_directory_name}/'
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as gitignore:
                lines = gitignore.readlines()
            if any(ignore_line in line for line in lines):
                return
        with open(gitignore_path, 'a') as gitignore:
           gitignore.write(f'\n{ignore_line}\n')

    def create_output_directory(self) -> None:
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)
        self.add_ligne_gitignore()

    def find_python_files_in_directory(self) -> None:
        #TODO : enlever les fichier test
        for root, _, files in os.walk(self.target_directory):
            for file in files:
                if file.endswith(self.extension):
                    file_name, _ = os.path.splitext(file)
                    self.files_in_directory.append(file_name)
                    self.path_files_in_directory.append(os.path.join(root, file))

    def check_files_in_string(self, line: str):
        return all(file not in line for file in self.files_in_directory)

    def process_import_statement(self, line: str):
        if line.startswith(("import","from")):
            if line not in self.imports and self.check_files_in_string(line):
                self.imports.append(line)

    def process_main_file(self, path: str, file: list):
        docstring_started = False
        inside_docstring = False
        for line in file:
            self.process_import_statement(line)
            striped_line = line.strip()
            if not docstring_started:
                if striped_line == '"""':
                    inside_docstring = not inside_docstring
                    if not inside_docstring:
                        docstring_started = True
                    self.presentation.append(line)
                    continue
                if inside_docstring:
                    self.presentation.append(line)
                    continue
            if not line.startswith(("import","from")):
                self.main_file_content.append(line)
                continue

    def process_other_files(self, line: str):
            if not line.startswith(("import", "from")):
                self.other_files_content.append(line)

    def part_content_in_variable(self):
        for path in self.path_files_in_directory:
            if not path.endswith(self.output_file_name):
                with open(path, "r") as file:
                    if path.endswith("__main__.py"):
                        self.process_main_file(path, file)
                    else:
                        for line in file:
                            self.process_import_statement(line)
                            self.process_other_files(line)

    def merge_variables_in_new_file(self):
        with open(self.output_file_path,"w") as output_file:
            output_file.writelines(self.presentation)
            output_file.writelines(self.imports)
            output_file.writelines(self.other_files_content)
            output_file.writelines(self.main_file_content)

    def script_merger(self):
        self.create_output_directory()
        self.find_python_files_in_directory()
        self.part_content_in_variable()
        self.merge_variables_in_new_file()

    def show_result(self):
        self.label.config(text = "Script exécuté avec succès !")
        match self.os:
            case "Windows":
                os.system(f'explorer "{os.path.abspath(self.output_directory_path)}"')
            case "Darwin":
                os.system(f'open "{os.path.abspath(self.output_directory_path)}"')