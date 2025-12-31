from templates import Config
from utils.dir_utils import pick_folder
import os

class SourceConfig(Config):
    def prompt_config(self):
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
        
        return src

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        return config_value
