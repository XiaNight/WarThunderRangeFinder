import tkinter as tk

class Interface:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x600")

    def add_label(self, text, row, column):
        stringVar = tk.StringVar(value=text)
        label = tk.Label(self.window, textvariable=stringVar)
        label.grid(row=row, column=column)
        return stringVar

    def add_entry(self, row, column, width=10):
        entry_var = tk.StringVar()
        entry = tk.Entry(self.window, textvariable=entry_var, width=width)
        entry.grid(row=row, column=column)
        return entry_var

    def add_int_entry(self, row, column, width=10):
        int_var = tk.IntVar()
        entry = tk.Entry(self.window, textvariable=int_var, width=width)
        entry.grid(row=row, column=column)
        return int_var

    def add_float_entry(self, row, column, width=10):
        float_var = tk.DoubleVar()
        entry = tk.Entry(self.window, textvariable=float_var, width=width)
        entry.grid(row=row, column=column)
        return float_var

    def add_checkbox(self, text, row, column):
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.window, text=text, variable=checkbox_var)
        checkbox.grid(row=row, column=column)
        return checkbox_var

    def add_button(self, text, row, column, command):
        button = tk.Button(self.window, text=text, command=command)
        button.grid(row=row, column=column)

    def run(self):
        self.window.mainloop()

def save_settings():
    print("Text:", text_var.get())
    print("Number:", int_var.get())
    print("Checkbox:", checkbox_var.get())

# interface = Interface("Settings")

# interface.add_label("Text:", 0, 0)
# text_var = interface.add_entry(0, 1)

# interface.add_label("Number:", 1, 0)
# int_var = interface.add_int_entry(1, 1)

# interface.add_label("Checkbox:", 2, 0)
# checkbox_var = interface.add_checkbox("Enable", 2, 1)

# interface.add_button("Save", 3, 0, save_settings)
# interface.add_button("Quit", 3, 1, interface.window.quit)

# interface.run()