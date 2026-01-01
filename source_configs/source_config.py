from templates import Config
from utils.dir_utils import pick_folder
from .registry import register
import os
import textoutputcontroller as toc

@register
class SourceConfig(Config):
    def prompt(self, prev_config_value):
        answer = input(
                "Assign a folder to back up? [Enter Y/n]: "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            return "(No Value)"

        src = pick_folder("Select folder to backup")

        if not src or not os.path.isdir(src):
            return "(No Value)"
        
        return src

    def resolve_helper(self, resolve_params):
        if self.config_value == "(No Value)":
            return []

        if not os.path.isdir(resolve_params.config_value):
            toc.error(f"The source {resolve_params.config_value} doesn't exist. Did your folder structure change ? Please reset your source.")
            self.load_prompt_and_save()

        return ([self.config_value] if self.config_value != "(No Value)" else [])
