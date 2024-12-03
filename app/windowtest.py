import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module

root = tkinterDnD.Tk()
root.title("CSV Dropper")

stringvar = tk.StringVar()
stringvar.set('Suelta tu CSV aquí!')

selected_file = None  # To store the file path


def drop(event):
    global selected_file
    selected_file = event.data.strip()  # Save the file path
    stringvar.set(f"Archivo seleccionado: {selected_file}")
    root.after(1000, root.destroy)  # Close the window after 1 second


label_2 = ttk.Label(
    root, ondrop=drop, textvar=stringvar, padding=50, relief="solid"
)
label_2.pack(fill="both", expand=True, padx=10, pady=10)

def get_selected_file():
    root.mainloop()  # Keep running the GUI
    return selected_file
