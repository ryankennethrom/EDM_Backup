from templates import Config
from utils.dir_utils import pick_folder
from utils.config_utils import get_config
import textoutputcontroller as toc
from .registry import register
import ast
import os

@register
class PrefixDestinationConfig(Config):
    def prompt(self, prev_config_value):
        # Pre-populate table from existing config (string → dict)
        try:
            table = ast.literal_eval(prev_config_value) if prev_config_value is not None else dict()
        except (ValueError, SyntaxError):
            table = dict()

        while True:
            print("Current prefix --> destination mappings:")
            if table:
                for i, (prefix, folder) in enumerate(table.items(), 1):
                    print(f"  {i}. '{prefix}' --> {folder}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a prefix")
            print("  [D] Delete a prefix")
            print("  [S] Save & Stop")

            choice = input("> ").strip().lower()

            # ADD PREFIX
            if choice in ("a", "add"):
                prefix = input("Enter the prefix: ").strip()
                if not prefix:
                    print("Prefix cannot be empty.")
                    continue
                dst_folder = pick_folder(f"Select destination folder for prefix '{prefix}'")
                if dst_folder:
                    table[prefix] = dst_folder

            # DELETE PREFIX
            elif choice in ("d", "delete"):
                if not table:
                    print("No prefixes to delete.")
                    continue
                prefix = input("Enter the prefix to delete: ").strip()
                if prefix in table:
                    del table[prefix]
                    print(f"Deleted prefix '{prefix}'.")
                else:
                    print(f"Prefix '{prefix}' not found.")

            # STOP
            elif choice in ("s", "stop", ""):
                break

            else:
                print("Invalid choice. Enter A, D, or S.")

        # Return as string for storage
        return str(table)

    def resolve_helper(self, resolve_params):
        config = ast.literal_eval(self.config_value)
        for key, folder in config.items():
            if resolve_params.src_filename.startswith(key):
                toc.info(f"Prefix '{key}' matched with {resolve_params.src_filename}")
                if not os.path.isdir(folder):
                    toc.error(f"The destination folder '{folder}' of the prefix '{key}' does not exist. Did your folder structure change ? Please replace the folder or remove the prefix, ")
                    self.load_prompt_and_save()
                    self.resolve_helper(resolve_params)
                    break
                return folder

        return resolve_params.dst_dirpath
