from templates import Config
from .registry import register
import ast
import textoutputcontroller as toc

@register
class SkipDestinationUndefinedConfig(Config):

    def prompt(self, prev_config_value):
        answer = input(
                "Skip files with undefined destination ? [Enter Y/n] "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            return "False"
        else:
            return "True"

    def resolve_helper(self, resolve_params):
        enabled = ast.literal_eval(resolve_params.config_value)
        
        if not enabled and resolve_params.dst_dirpath == "":
            toc.info(f"Failed to back up the file '{resolve_params.src_filepath}'. Could not resolve destination. Notify Ryan or whoever is maintaining the backup scripts. Press enter to continue.")
            input()
            return True
        
        if enabled and resolve_params.dst_dirpath == "":
            return True

        return False
