from templates import Config
from utils.dir_utils import pick_folder
import textoutputcontroller as toc
from .registry import register
import ast

@register
class PrefixDestinationConfig(Config):
    def prompt_config(self):
        table = dict()
        while input(
                "Set a destination folder to a specific file prefix ? [Enter Y/n] " if len(table) <= 0 else "Set another prefix-destination config ? [Enter Y/n] "
                ).strip().lower() in ("", "y", "yes"):
            prefix = input(
                    "Enter the prefix: "
                    )
            dst_folder = pick_folder("Select destination folder")
            table[prefix] = dst_folder
        return str(table)

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        config = ast.literal_eval(config_value)
        for key in config.keys():
            if source_filename.startswith(key):
                toc.info(f"Prefix '{key}' matched with {source_filename}")
                return config[key]
        return prov_dst_dir

