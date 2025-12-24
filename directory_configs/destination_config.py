from .registry import register
from templates import BackupPathConfig
from utils.dir_utils import pick_folder

@register
class DestinationConfig(BackupPathConfig):
    def prompt_config(self):
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

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        return config_value
