from templates import Config
from .registry import register
from utils.dir_utils import pick_foldername
from utils.config_utils import get_config
import ast
import os


@register
class SkipFolderNamesConfig(Config):

    def prompt(self, prev_config_value):
        """
        Interactive interface for managing a list of foldernames.
        """
        selected_foldernames = ast.literal_eval(prev_config_value) if prev_config_value is not None else []

        while True:
            print("\nCurrent folders to be skipped :")
            if selected_foldernames:
                for i, f in enumerate(selected_foldernames, 1):
                    print(f"  {i}. {f}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a folder name to skip")
            print("  [D] Remove a folder name")
            print("  [S] Save & Stop")

            choice = input("> ").strip().lower()

            # ADD FILE
            if choice in ("a", "add"):
                foldername = pick_foldername("Select a folder name to add")
                if foldername and foldername not in selected_foldernames:
                    selected_foldernames.append(foldername)

            # DELETE FILE
            elif choice in ("d", "delete"):
                if not selected_foldernames:
                    print("No files to delete.")
                    continue

                foldername = pick_foldername("Select a folder name to remove")
                if foldername in selected_foldernames:
                    selected_foldernames.remove(foldername)

            # STOP
            elif choice in ("s", "stop", ""):
                break

            else:
                print("Invalid choice.")

        # Store as a simple string (easy to persist)
        return str(selected_foldernames)

    def resolve_helper(self, resolve_params):
        """
        If the source foldername is in the skip list, generate a unique path.
        Otherwise, overwrite.
        """

        skip_foldernames = ast.literal_eval(resolve_params.config_value)

        if resolve_params.src_filename in skip_foldernames:
            return True

        return False
