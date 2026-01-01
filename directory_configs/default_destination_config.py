from templates import Config
from .registry import register
from utils.dir_utils import pick_folder
import os
import textoutputcontroller as toc

@register
class DefaultDestinationConfig(Config):
    def prompt(self, prev_config_value):
        answer = input(
            "Assign a default destination folder ? [Enter Y/n] "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            dst = pick_folder("Select folder to store backed up files")

            if not dst:
                return "(No Value)"

            return dst
        else:
            return "(No Value)"
        
        return dst

    def resolve_helper(self, resolve_params):
        if self.config_value != "(No Value)" and resolve_params.dst_dirpath == "":
            if not os.path.isdir(self.config_value):
                toc.error(f"The destination folder {self.config_value} does not exist. Did your folder structure change ? Please replace or remove your default destination folder.")
                self.load_prompt_and_save()
                return self.resolve_helper(resolve_params)

            return self.config_value
        
        return resolve_params.dst_dirpath
