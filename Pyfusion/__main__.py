import tkinter as tk
import ttkbootstrap as ttk
import platform
from typing import Union

from utils import is_os_light_mode
from script_fusion.script_fusion_app import ScriptFusionApp
from class_separator.class_separator_app import ClassSeparatorApp
from class_separator.TreeStructureApp import TreeStructureApp


class Main(ttk.Window):
    def __init__(self, os: str) -> None:
        self.os: str = os
        theme: str = "flatly" if is_os_light_mode(self.os) else "darkly"
        super().__init__(themename = theme)
        self.title("Script Merger")
        self.resizable(False, False)
        self.create_interface()

    def create_interface(self) -> None:
        self.app_frame: ttk.Frame = ttk.Frame(self)
        self.frame: AppChoiceApp | ClassSeparatorApp | TreeStructureApp = AppChoiceApp(self.app_frame)
        self.button_frame: ttk.Frame = ttk.Frame(self)
        self.back_button: ttk.Button = ttk.Button(self.button_frame, text = "Quit", command = self.destroy)
        self.place_widget()

    def place_widget(self) -> None:
        self.app_frame.grid(row = 0, column = 0)
        self.button_frame.grid(row = 1, column = 0)
        self.back_button.pack()

    def go_to_new_app(self, app: ClassSeparatorApp | ScriptFusionApp | TreeStructureApp, dict: dict = None) -> None:
        self.frame.destroy()
        match app.__name__ :
            case "ScriptFusionApp" | "ClassSeparatorApp":
                self.frame: Union[ClassSeparatorApp, ScriptFusionApp, TreeStructureApp] = app(self.app_frame, self.os)
                self.back_button.config(command = self.return_to_app_choice)
            case "TreeStructureApp":
                self.frame: Union[ClassSeparatorApp, ScriptFusionApp, TreeStructureApp] = app(self.app_frame, dict)
                self.back_button.config(command = lambda: self.go_to_new_app(ClassSeparatorApp))
        self.back_button.config(text = "retour")

    def return_to_app_choice(self) -> None:
        self.frame.destroy()
        self.frame: AppChoiceApp = AppChoiceApp(self.app_frame)
        self.back_button.config(text = "Quit", command = self.destroy)

class AppChoiceApp(ttk.Frame):
    def __init__(self, master: ttk.Frame) -> None:
        self.master: ttk.Frame = master
        super().__init__(self.master)
        self.create_widgets()
        self.pack()

    def create_widgets(self) -> None:
        master: Main = self.master.master
        self.merged_button: ttk.Button = ttk.Button(self,text = "ScritpFusion", command = lambda: master.go_to_new_app(ScriptFusionApp))
        self.separator_button: ttk.Button = ttk.Button(self,text = "ClassSeparator", command = lambda: master.go_to_new_app(ClassSeparatorApp))
        self.place_widgets()

    def place_widgets(self) -> None:
        self.merged_button.pack(padx = 25, pady = (25, 7), fill = tk.BOTH)
        self.separator_button.pack(padx = 25, pady = (7, 25), fill = tk.BOTH)

if __name__ == "__main__":
    os: str = platform.system()
    app: ttk.Window = Main(os)
    app.mainloop()