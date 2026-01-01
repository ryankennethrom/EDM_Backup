import tkinter as tk
from tkinter import filedialog
import os

def pick_filename(title):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    path = filedialog.askopenfilename(title=title)

    root.destroy()

    if not path:
        return ""

    return os.path.basename(path)

def pick_folder(title):
    root = tk.Tk()
    root.withdraw()  # hide main window
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder

def pick_foldername(prompt="Select a folder"):
    """
    Opens a folder picker dialog and returns only the folder NAME,
    not the full path.

    Returns None if the user cancels.
    """
    # Hide the main Tkinter window
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # bring dialog to front

    folder_path = filedialog.askdirectory(title=prompt)

    if not folder_path:
        return None

    # Return only the folder name (last part of the path)
    folder_name = os.path.basename(os.path.normpath(folder_path))
    return folder_name
