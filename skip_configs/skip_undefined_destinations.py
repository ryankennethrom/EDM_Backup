from templates import Config
from .registry import register
import ast
import textoutputcontroller as toc

@register
class SkipDestinationUndefinedConfig(Config):
    def get_settings_description(self):
        return "Skip backup a file if the script doesn't know where it should go ?"

    def prompt(self, prev_config_value):
        answer = input(
                f"{self.get_settings_description()} [Enter Y/n] "
        ).strip().lower()

        if answer not in ("", "y", "yes"):
            return "False"
        else:
            return "True"

    def on_undefined_destination_detected(self, resolve_params):
        toc.error(f"Failed to back up the file. Could not resolve destination. Notify Ryan or whoever is maintaining the backup scripts. Press enter to continue.")
        input()
        return True
    
    # Return True to skip backing up the file
    def resolve_helper(self, resolve_params):
        enabled = ast.literal_eval(resolve_params.config_value)
        
        if not enabled and resolve_params.dst_dirpath == "":
            return self.on_undefined_destination_detected(resolve_params)
        
        if enabled and resolve_params.dst_dirpath == "":
            return True

        return False
