import os
import ttkbootstrap as ttk


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
        files_in_directory (list): List of Python script file names (without extension).
        path_files_in_directory (list): List of paths to Python script files.
        import_statements (list): List of import statements.

    Methods:
        __init__(folder_entry: ttk.Entry, result_label: ttk.Label): Initialize the ScriptFusion .
        create_output_directory(): Create the output directory if it doesn't exist.
        find_python_files_in_directory(): Find Python script files in the target directory.
        check_files_in_string(line: str): Check if any file from files_in_directory is present in the line.
        process_import_statement(line: str): Process import statements in the line.
        process_script_content(line, path): Process script content based on the line and path.
        process_content(): Process the content of script files.
        merge_script_files(): Merge the script files into the output file.
        start_script_merger(): Start the script merging process.
        get_result(): Update the result label with the execution status.
    """
    def __init__(self, folder_entry: ttk.Entry, result_label: ttk.Label, extension = ".py"):
        """
        Initialize the ScriptFusion .

        Args:
            folder_entry (ttk.Entry): Entry widget containing the target directory.
            result_label (ttk.Label): Label widget to display execution results.

        Returns:
            None
        """
        self.root_directory = folder_entry.get()
        self.target_directory = self.find_script_directory()
        self.label = result_label
        self.extension = extension
        if self.check_input():
            self.output_directory_name = "merged_scripts"
            self.output_file_name = "merged_scripts.py"
            self.output_directory_path = os.path.join(self.target_directory, self.output_directory_name)
            self.output_file_path = os.path.join(self.output_directory_path,self.output_file_name)
            self.files_in_directory = []
            self.path_files_in_directory = []
            self.import_statements = []
            self.main_file_content = []
            self.script_content = []
            self.start_script_merger()
            self.get_result()

    def find_script_directory(self):
        target_base_name = os.path.basename(self.root_directory)
        for root, dirs, _ in os.walk(self.root_directory):
            if target_base_name in dirs:
                print("ok")
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
    
    def add_ligne_gitignore(self):
        gitignore_path = os.path.join(self.root_directory, '.gitignore')        
        ignore_line = f'{self.output_directory_name}/'
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                lines = f.readlines()
            if any(ignore_line in line for line in lines):
                return        
        with open(gitignore_path, 'a') as f:
           f.write(f'\n{ignore_line}\n')

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
        self.add_ligne_gitignore()

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
                    self.files_in_directory.append(file_name)
                    self.path_files_in_directory.append(os.path.join(root, file))

    def check_files_in_string(self, line: str):
        """
        Check if any file from files_in_directory is present in the line.

        Args:
            line (str): Line of text to check.

        Returns:
            bool: True if none of the files in files_in_directory are present, False otherwise.
        """
        return all(file not in line for file in self.files_in_directory)
    
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
            if line not in self.import_statements and self.check_files_in_string(line):
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
            if path.endswith("__main__.py"):
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
        
        for path in self.path_files_in_directory:
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
        
        self.create_output_directory()
        self.find_python_files_in_directory()
        self.process_content()
        self.merge_script_files()

    def get_result(self):
        """
        Update the result label with the execution status.

        Args:
            None

        Returns:
            None
        """
        self.label.config(text = "Script exécuté avec succès !")
        os.system(f'explorer "{os.path.abspath(self.output_directory_path)}"')
