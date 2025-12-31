from templates import Config
from .registry import register
from utils.dir_utils import pick_folder

@register
class DefaultDestinationConfig(Config):
    def prompt(self, prev_config_value):
        answer = input(
            "Assign a default destination folder ? [Enter Y/n] "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            dst = pick_folder("Select folder to store backed up files")

            if not dst:
                raise SystemExit("No destination folder selected. Exiting.")

            return dst
        else:
            raise SystemExit("Destination folder not set. Exiting.")
        
        return dst

    def resolve_helper(self, source_filename, source_filepath, prov_dst_dir, config_value):
        if prov_dst_dir != "":
            return prov_dst_dir
        return config_value
