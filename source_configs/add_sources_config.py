from templates import Config
from utils.dir_utils import pick_folder
from .registry import register
import os

@register
class AdditionalSourcesConfig(Config):
    def prompt(self, prev_config_value):
        answer = input(
            "Do you have additional sources to backup? [Enter Y/n]: "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            raise SystemExit("No source folder assigned. Exiting.")

        sources = []

        while True:
            src = pick_folder("Select folder to backup (Cancel to finish)")

            if not src:
                break  # user cancelled → done selecting

            if not os.path.isdir(src):
                print("Selected path is not a directory. Skipping.")
                continue

            if src in sources:
                print("Folder already added. Skipping.")
                continue

            sources.append(src)

            more = input("Add another folder? [Enter Y/n]: ").strip().lower()
            if more not in ("", "y", "yes"):
                break

        if not sources:
            raise SystemExit("No folders selected. Exiting.")

        # Return as STRING so it can be stored in config
        return str(sources)

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        return ast.literal_eval(config_value) if config_value is not None else []
