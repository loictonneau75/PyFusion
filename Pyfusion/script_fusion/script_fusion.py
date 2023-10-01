import os
import ttkbootstrap as ttk


class ScriptFusion ():
    """
    ScriptFusion class for merging Python script files.

    Attributes:
        extension (str): The file extension to look for.
        target_directory (str): The target directory for script files.
        output_directory_name (str): The name of the output directory.
        output_directory_path (str): The path to the output directory.
        output_file_name (str): The name of the merged output file.
        output_file_path (str): The path to the merged output file.
        files_in_directory (list): List of Python script filenames (without extension).
        path_files_in_directory (list): List of paths to the Python script files.
        import_statements (list): List of import statements.

    Methods:
        __init__(folder_entry: ttk.Entry, result_label: ttk.Label): Initializes ScriptFusion.
        find_script_directory(): Finds the script directory based on the basename of the root directory.
        check_input(): Validates the input directory.
        initialize_directories_and_files(): Initializes the names and paths for the output directory and file.
        add_line_to_gitignore(): Adds the output directory name to the `.gitignore` file in the root directory.
        create_output_directory(): Creates the output directory if it doesn't exist.
        find_python_files_in_directory(): Finds Python script files in the target directory.
        check_files_in_string(line: str): Checks if a file from files_in_directory is present in the line.
        process_import_statement(line: str): Processes the import statements in the line.
        process_main_file(path, file): Processes the content of a "__main__.py" file to extract docstrings and non-import lines.
        process_other_files(line, path): Processes the script content based on the line and path.
        part_content_into_variable(): Processes the content of script files.
        merge_variables_into_new_file(): Merges the script files into the output file.
        script_merger(): Initiates the script merging process.
        show_result(): Updates the result label with the execution status.
    """
    def __init__(self, folder_entry: ttk.Entry, result_label: ttk.Label, extension = ".py"):
        """
        Initialize the ScriptFusion object.

        Args:
            folder_entry (ttk.Entry): The Entry widget containing the target directory path.
            result_label (ttk.Label): The Label widget for displaying execution results.
            extension (str, optional): The file extension to look for. Defaults to ".py".

        Returns:
            None
        """
        self.root_directory = folder_entry.get()
        self.target_directory = self.find_script_directory()
        self.label = result_label
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

    def find_script_directory(self):
        """
        Find the script directory based on the basename of the root directory.

        Recursively traverses from the root directory to find a sub-directory 
        with the same name as the basename of the root directory.

        Args:
            None

        Returns:
            str: The absolute path of the script directory if found; otherwise, the root directory.
        """
        target_base_name = os.path.basename(self.root_directory)
        for root, dirs, _ in os.walk(self.root_directory):
            if target_base_name in dirs:
                return os.path.join(root, target_base_name)
        return self.root_directory

    def check_input(self) -> bool:
        """
        Validate the input directory.

        Checks whether the `self.target_directory` is set and whether it exists 
        in the file system. Updates `self.label` with relevant status messages.

        Args:
            None

        Returns:
            bool: True if `self.target_directory` is set and exists, False otherwise.
        """
        if not self.target_directory:
            self.label.config(text = "Veuillez inscrire un dossier !")
            return False
        if not os.path.exists(self.target_directory):
            self.label.config(text = "Le chemin spécifié n'existe pas !")
            return False
        return  True
    
    def initialize_directories_and_files(self):
        """
        Initialize names and paths for the output directory and file.

        Sets `self.output_directory_name`, `self.output_file_name`, `self.output_directory_path`, 
        and `self.output_file_path` based on `self.target_directory`.

        Args:
            None

        Returns:
            None
        """
        self.output_directory_name = "merged_scripts"
        self.output_file_name = "merged_scripts.py"
        self.output_directory_path = os.path.join(self.target_directory, self.output_directory_name)
        self.output_file_path = os.path.join(self.output_directory_path,self.output_file_name)
        
    def add_ligne_gitignore(self):
        """
        Add the output directory name to the `.gitignore` file in the root directory.

        If the `.gitignore` file exists, checks whether the output directory is already ignored.
        If not, appends the directory name to `.gitignore`.

        Args:
            None

        Returns:
            None
        """
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

    def process_import_statement(self, line: str):
        """
        Process import statements in the provided line.

        Checks whether the import statement already exists in the list of
        collected import statements, and if the statement doesn't refer to any
        of the files in the target directory.

        Args:
            line (str): The line containing the import statement.

        Returns:
            None
        """
        if line.startswith(("import","from")):
            if line not in self.imports and self.check_files_in_string(line):
                self.imports.append(line)

    def process_main_file(self, path: str, file: list):
        """
        Process the main Python file to extract docstrings and non-import lines.

        Extracts docstrings and appends them to `self.presentation`. Also
        collects non-import lines and appends them to `self.main_file_content`.

        Args:
            path (str): The full path to the Python file being processed.
            file (iterable): An iterable containing the lines of the file.

        Returns:
            None
        """
        docstring_started = False
        inside_docstring = False

        if path.endswith("__main__.py"):
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

    def process_other_files(self, line: str, path: str):
        """
        Process the content of other Python files.

        Ignores import statements and appends the remaining lines to 
        `self.other_files_content`.

        Args:
            line (str): The line to process.
            path (str): The path of the file containing the line.

        Returns:
            None
        """
        if not path.endswith("__main__.py"):
            if not line.startswith(("import", "from")):
                self.other_files_content.append(line)

    def part_content_in_variable(self):
        """
        Process the content of all script files and divide it into variables.

        Args:
            None

        Returns:
            None
        """
        for path in self.path_files_in_directory:
            if not path.endswith(self.output_file_name):
                with open(path, "r") as file:
                    self.process_main_file(path, file)
                    for line in file:
                        self.process_import_statement(line)
                        self.process_other_files(line, path)

    def merge_variables_in_new_file(self):
        """
        Merge collected script content into a new file.

        Writes the processed lines from the presentation, imports, and content of 
        other files into a new output file.

        Args:
            None

        Returns:
            None
        """
        with open(self.output_file_path,"w") as output_file:
            output_file.writelines(self.presentation)
            output_file.writelines(self.imports)
            output_file.writelines(self.other_files_content)
            output_file.writelines(self.main_file_content)

    def script_merger(self):
        """
        Start the script merging process.

        Calls various internal methods to find Python files in the target directory,
        process their content, and write it into a new merged file.

        Args:
            None

        Returns:
            None
        """
        self.create_output_directory()
        self.find_python_files_in_directory()
        self.part_content_in_variable()
        self.merge_variables_in_new_file()

    def show_result(self):
        """
        Update the result label with the execution status.

        Sets the text of `self.label` to indicate the success of the script
        execution and opens the output directory.

        Args:
            None

        Returns:
            None
        """
        self.label.config(text = "Script exécuté avec succès !")
        os.system(f'explorer "{os.path.abspath(self.output_directory_path)}"')
