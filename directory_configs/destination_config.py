from .registry import register
from templates import Config
from utils.dir_utils import pick_folder

@register
class DestinationConfig(Config):
    def prompt(self, prev_config_value):
        answer = input(
            "Script doesn't know where to back up files.\n"
            "Assign destination folder? [Enter Y/n]: "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            dst = pick_folder("Select folder to store backed up files")

            if not dst:
                raise SystemExit("No destination folder selected. Exiting.")
            
            return dst
        else:
            raise SystemExit("Destination folder not set. Exiting.")

    def resolve_helper(self, resolve_params):
        return resolve_params.config_value
