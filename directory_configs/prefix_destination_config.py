from templates import Config
from utils.dir_utils import pick_folder
from utils.config_utils import get_config
import textoutputcontroller as toc
from .registry import register
import ast

@register
class PrefixDestinationConfig(Config):
    def prompt(self, prev_config_value):
        # Pre-populate table from existing config (string → dict)
        try:
            table = ast.literal_eval(prev_config_value) if prev_config_value is not None else dict()
        except (ValueError, SyntaxError):
            table = dict()

        while True:
            print("\nCurrent prefix → destination mappings:")
            if table:
                for i, (prefix, folder) in enumerate(table.items(), 1):
                    print(f"  {i}. '{prefix}' → {folder}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a prefix")
            print("  [D] Delete a prefix")
            print("  [S] Stop")

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

    def resolve_helper(self, source_filename, source_filepath, prov_dst_dir, config_value):
        config = ast.literal_eval(config_value)
        for key, folder in config.items():
            if source_filename.startswith(key):
                toc.info(f"Prefix '{key}' matched with {source_filename}")
                return folder
        return prov_dst_dir
