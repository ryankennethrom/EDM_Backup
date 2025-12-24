from config_utils import get_config, overwrite_config
from dir_utils import pick_folder
import os

class SOURCE:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self):
        config = get_config()

        if "SOURCE" not in config or not os.path.isdir(config["SOURCE"]):
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

            config["SOURCE"] = src

            overwrite_config(config)

        return config["SOURCE"]


