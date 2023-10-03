import ttkbootstrap as ttk
import os
import re

from class_separator.TreeStructureApp import TreeStructureApp

class ClassSeparator():
    def __init__(self, master, file_entry: ttk.Entry, folder_entry: ttk.Entry, result_label: ttk.Label, extension = ".py") -> None:
        self.file = file_entry.get()
        self.folder = folder_entry.get()
        self.label = result_label
        self.extension = extension
        if self.check_input():
            self.dockstring = []
            self.imports = {}
            self.starting_snippet = []
            self.classes ={}
            self.utils = {}
            self.file_separator()
            master.master.go_to_new_app(TreeStructureApp)

    def check_input(self) -> bool:
        if not self.file:
            self.label.config(text = "Veuillez inscrire un fichier !")
            return False
        if not os.path.exists(self.file):
            self.label.config(text = "Le chemin du fichier spécifié n'existe pas !")
            return  False

        if not self.folder:
            self.label.config(text = "Veuillez inscrire un dossier !")
            return False
        if not os.path.exists(self.folder):
            self.label.config(text = "Le chemin du dossier spécifié n'existe pas !")
            return False
        return True

    def file_separator(self):
        docstring_started = False
        inside_docstring = False
        with open(self.file, "r") as file:
            text = file.read().strip().split('\n')
            self.process_dockstring_statement(text,docstring_started, inside_docstring)
            self.process_import_statement(text)
            self.process_starting_snippet_statement(text)
            self.process_class_statement(text)
            self.process_functions_statement(text)
            #print(f"docstring\n{self.dockstring}\nimport\n{list(self.imports.keys())}\nstart snippet\n{self.starting_snippet}\nutils\n{list(self.utils.keys())}\nclass\n{list(self.classes.keys())}")

    def process_dockstring_statement(self, text: list, is_started: bool, is_inside: bool) -> None:
        for line in text:
            if not is_started:
                if line == '"""':
                    is_inside = not is_inside

                    if not is_inside:
                        is_started = True

                    self.dockstring.append(line)
                    continue

                if is_inside:
                    self.dockstring.append(line)
                    continue

    def process_import_statement(self, text: list) -> None:
        for line in text:
            if line.startswith("from"):
                _, module, _, names = line.split(None, 3)
                for name in names.split(','):
                    key = name.strip()
                    self.imports[key] = line
            elif line.startswith("import"):
                key = line.split()[-1]
                self.imports[key] = line

    def process_starting_snippet_statement(self, text: list) -> None:
        found_snippet = False
        for i, line in enumerate(text):
            if re.match(r'if __name__ == ["\']__main__["\']:', line):
                found_snippet = True
                self.starting_snippet.append(line)
                j = i + 1
                while j < len(text) and text[j] != "":
                    self.starting_snippet.append(text[j])
                    j += 1
        if found_snippet:
            self.starting_snippet = "\n".join(self.starting_snippet)
        else:
            self.starting_snippet = None

    def process_class_statement(self, text: list) -> None:
        inside_class = False
        current_class_content = []
        class_name = None

        for line in text:
            stripped_line = line.strip()

            if line in self.dockstring or line in self.imports or line in self.starting_snippet:
                continue

            if stripped_line.startswith("class "):
                if inside_class:
                    self.classes[class_name] = current_class_content
                    current_class_content = []

                class_name = stripped_line.split(':')[0].split()[1]
                class_name = re.sub(r'\(.*\)', '', class_name)
                class_name = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', class_name).lower()
                inside_class = True

            if inside_class:
                current_class_content.append(line)

        if current_class_content:
            self.classes[class_name] = current_class_content

    def process_functions_statement(self, text: list) -> None:
        inside_function = False
        current_function_content = []
        function_name = None

        for i, line in enumerate(text):
            stripped_line = line.strip()

            if line in self.dockstring or line in self.imports or line in self.starting_snippet:
                continue

            if stripped_line.startswith("def "):
                if inside_function:
                    self.utils[function_name] = current_function_content
                    current_function_content = []

                indent_level = len(line) - len(line.lstrip())
                is_inside_class = any(text[j].strip().startswith("class ") and len(text[j]) - len(text[j].lstrip()) < indent_level for j in range(i))

                if not is_inside_class:
                    function_name = stripped_line.split('(')[0].split()[1]
                    inside_function = True

            if inside_function:
                current_function_content.append(line)

            if stripped_line.startswith("class ") and inside_function:
                self.utils[function_name] = current_function_content
                current_function_content = []
                inside_function = False

        if current_function_content:
            self.utils[function_name] = current_function_content
