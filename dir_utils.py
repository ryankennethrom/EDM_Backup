import tkinter as tk
from tkinter import filedialog

def pick_folder(title):
    root = tk.Tk()
    root.withdraw()  # hide main window
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder
