# Script Merger App

The Script Merger App is a Python application that allows you to merge multiple Python script files within a specified directory into a single output file.

## Features

- Choose a target directory containing Python script files.
- Automatically detect import statements and merge them.
- Create a merged output file named "test.py" in a subdirectory named "test".
- User-friendly graphical interface using `tkinter` and `ttkbootstrap`.

## Getting Started

1. Clone or download the repository to your local machine.

```bash
git clone https://github.com/loictonneau75/merger_file.git
```

2. Install the required packages using `pip`:

```bash
pip install ttkbootstrap
```

## Run

1. Run the script_merger_app.py script:

```bash
python script_merger_app.py
```
2. The GUI application will open, allowing you to select a target directory and merge the script files.

## Usage

1. Launch the application using the steps mentioned in the "Getting Started" section.

2. Click the "Parcourir" button to select the target directory containing the Python script files you want to merge.

3. Click the "Éxécuter" button to initiate the merging process.

4. The merged script file named "test.py" will be created in a subdirectory named "test" within the selected directory.

## Dependencies

- Python 3.x
- ttkbootstrap
- tkinter (usually included with Python)

## License

This project is licensed under the MIT License.

## Author

TONNEAU Loïc

## Acknowledgments

- This project was inspired by the need to efficiently merge multiple Python script files into a single output file.
- The application uses the ttkbootstrap library to create a modern and visually appealing GUI.