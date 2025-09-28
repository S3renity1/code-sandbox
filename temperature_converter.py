import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

@dataclass
class Temperature:
    celsius: float

    def __format__(self, format_spec: str) -> str:
        conversions = {
            'c': f"{self.celsius:.2f}°C",
            'f': f"{self.celsius * 9 / 5 + 32:.2f}°F",
            'k': f"{self.celsius + 273.15:.2f}K"
        }
        return conversions.get(format_spec, f"{self.celsius:.2f}°")

class TemperatureConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Converter")
        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="Enter temperature in Celsius:").grid(row=0, column=0, padx=10, pady=10)

        self.entry = ttk.Entry(self.root)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        convert_btn = ttk.Button(self.root, text="Convert", command=self.convert)
        convert_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.result_vars = {
            'c': tk.StringVar(),
            'f': tk.StringVar(),
            'k': tk.StringVar()
        }

        for i, unit in enumerate(['c', 'f', 'k'], start=2):
            ttk.Label(self.root, textvariable=self.result_vars[unit]).grid(row=i, column=0, columnspan=2)

    def convert(self):
        try:
            value = float(self.entry.get())
            temp = Temperature(value)
            for unit in self.result_vars:
                self.result_vars[unit].set(format(temp, unit))
        except ValueError:
            for var in self.result_vars.values():
                var.set("Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureConverterApp(root)
    root.mainloop()