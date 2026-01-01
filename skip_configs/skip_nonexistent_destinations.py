from templates import Config
from .registry import register
import ast
import textoutputcontroller as toc
import os

@register
class SkipNonExistentDestinationConfig(Config):

    def prompt(self, prev_config_value):
        answer = input(
                "Skip files with nonexistent destination ? [Enter Y/n] "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            return "False"
        else:
            return "True"

    def resolve_helper(self, resolve_params):
        enabled = ast.literal_eval(resolve_params.config_value)
        
        if not enabled and not os.path.isdir(resolve_params.dst_dirpath):
            toc.info(f"Failed to back up the file '{resolve_params.src_filepath}'. The destination doesn't exist. Notify Ryan or whoever is maintaining the backup scripts. Press enter to continue.")
            input()
            return True
        
        if enabled and not os.path.isdir(resolve_params.dst_dirpath):
            return True

        return False
