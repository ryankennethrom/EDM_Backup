import os
import shutil
import sys
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Pick a folder using file explorer
def pick_folder(title):
    root = tk.Tk()
    root.withdraw()  # hide main window
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder

# Read from config.txt
def get_configs():
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, "config.txt")

    if not os.path.isfile(config_path):
        return {}

    config = {}

    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key] = value
    return config

def overwrite_config(config):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, "config.txt")

    with open(config_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

def get_unique_path(dst_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = filename

    while os.path.exists(os.path.join(dst_dir, candidate)):
        candidate = f"{base}({counter}){ext}"
        counter += 1

    return os.path.join(dst_dir, candidate)

if __name__ == "__main__":

    configs = get_configs()

    # r"C:\EdmRackOut"

    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, "config.txt")

    print("Running EDM_Backup \n")
    
    print("If you're planning to change the script, go to EDM_Backup/Readme.md for more information.\n")

    print( f"If you want to redefine the configuration of the script, go to {config_path} and delete the config.txt file. Finally, run the exe file again. \n" if os.path.isfile(config_path) else ""
    )

    if "SOURCE" not in configs or not os.path.isdir(configs["SOURCE"]):
        answer = input(
                "Script doesn't know which folder to back up.\n"
                "Assign which folder to back up? [Enter Y/n]: "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            raise SystemExit("No source folder assigned. Exiting.")
        
        src = pick_folder("Select folder to backup")

        if not src:
            raise SystemExit("No folder selected. Exiting.")

        if not os.path.isdir(src):
            raise RuntimeError("Selected path is not a directory.")

        configs["SOURCE"] = src

        overwrite_config(configs)

    # r"Z:\PRODUCTION & LAB\Data Backup\TAN-TBN"

    if "DESTINATION" not in configs or not os.path.isdir(configs["DESTINATION"]):
        answer = input(
            "Script doesn't know where to back up files.\n"
            "Assign destination folder? [Enter Y/n]: "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            dst = pick_folder("Select folder to store backed up files")

            if not dst:
                raise SystemExit("No destination folder selected. Exiting.")

        else:
            raise SystemExit("Destination folder not set. Exiting.")
        
        configs["DESTINATION"] = dst
        overwrite_config(configs)
    
    if "ORGANIZE_BY_CURRENT_YEAR" not in configs:
        answer = input(
            "Scripts needs you to answer the following.\n"
            "Organize files by current year ? [Enter Y/n] "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            configs["ORGANIZE_BY_CURRENT_YEAR"] = "true"
        else:
            configs["ORGANIZE_BY_CURRENT_YEAR"] = "false"
        overwrite_config(configs)

    if "REPLACE_FILES" not in configs:
        answer = input(
            "Replace files in destination or keep copies?\n"
            "[Enter R to replace / C to keep copies] "
        ).strip().lower()

        if answer in ("", "r", "replace"):
            configs["REPLACE_FILES"] = "true"
        else:
            configs["REPLACE_FILES"] = "false"

        overwrite_config(configs)

    src = configs["SOURCE"]
    dst = configs["DESTINATION"]
    keep_copies = configs.get("REPLACE_FILES", "true") == "false"
    organize_by_current_year = configs.get("ORGANIZE_BY_CURRENT_YEAR") == "true"
    raw_excludes = configs.get("EXCLUDE_FILES", "")
    EXCLUDED_FILES = {
        name.strip().lower()
        for name in raw_excludes.split(",")
        if name.strip()
    }

    if organize_by_current_year:
        year = str(datetime.now().year)
        dst = os.path.join(dst, year)

    os.makedirs(dst, exist_ok=True)

    exe_path = os.path.abspath(sys.executable)

    for name in os.listdir(src):
        src_path = os.path.abspath(os.path.join(src, name))

        # Skip the running EXE
        if src_path == exe_path:
            continue

        if name.lower().endswith(".lnk"):
            continue

        if name.lower() in EXCLUDED_FILES:
            continue

        if not os.path.isfile(src_path):
            continue

        if keep_copies:
            # Auto-rename to h(1).txt, h(2).txt, etc.
            dst_path = get_unique_path(dst, name)
        else:
            # Replace existing file
            dst_path = os.path.join(dst, name)

        shutil.move(src_path, dst_path)  # ALWAYS deletes source
