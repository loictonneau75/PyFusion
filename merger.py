import os
from collections import defaultdict

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
    for word in word_list:
        if word in input_string:
            return False
    return True

def get_text(path_list: list, file_list: list):
    existing_import = []
    main = []
    scripts = []
    for path in path_list:
        if not path.endswith(output_filename):
            with open (path, "r") as file:
                    for line in file:
                        if line.startswith("import") or line.startswith("from"):
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

def create_test_file(file_path, imports, scripts):
    with open(file_path, "w") as output_file:
        output_file.writelines(imports)
        output_file.writelines(scripts)

def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    directory_path = r"C:\Users\loict\Desktop\pwd_managerV2"
    output_directory_name = "test"
    output_filename = "test.py"

    create_output_directory(os.path.join(directory_path, output_directory_name))
    file_path = os.path.join(directory_path, output_directory_name, output_filename)
    file_list, path_list = get_files_and_path(directory_path, ".py")
    imports, scripts = get_text(path_list, file_list)
    create_test_file(file_path, imports, scripts)

if __name__ == "__main__":
    main()
