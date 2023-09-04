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
        self.extension = ".py"
        self.target_directory = folder_entry.get()
        if not self.target_directory:
            result_label.config(text = "Veuillez inscrire un dossier !")
            return
        if not os.path.exists(self.target_directory):
            result_label.config(text = "Le chemin spécifié n'existe pas !")
            return
        self.start_script_merger()
        self.get_result(result_label)

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
        self.file_list = []
        self.path_list = []
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
