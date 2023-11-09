class TreeStructure():
    def __init__(self, data, widget):
        self.data = data
        self.widgets = widget
        print(f" data = {self.data.keys()}")
        print(f"label = {self.widgets.keys()}")
        print(f"combobox = {self.widgets.values()}")