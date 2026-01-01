from templates import Config
from .registry import register
from utils.dir_utils import pick_filename
from utils.config_utils import get_config
import ast
import os


@register
class SkipFileNamesConfig(Config):

    def prompt(self, prev_config_value):
        """
        Interactive interface for managing a list of file names.
        """
        selected_files = ast.literal_eval(prev_config_value) if prev_config_value is not None else []

        while True:
            print("\nCurrent file names to be skipped :")
            if selected_files:
                for i, f in enumerate(selected_files, 1):
                    print(f"  {i}. {f}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a file name to skip")
            print("  [D] Remove a file name")
            print("  [S] Save & Stop")

            choice = input("> ").strip().lower()

            # ADD FILE
            if choice in ("a", "add"):
                filename = pick_filename("Select a file name to add")
                if filename and filename not in selected_files:
                    selected_files.append(filename)

            # DELETE FILE
            elif choice in ("d", "delete"):
                if not selected_files:
                    print("No files to delete.")
                    continue

                filename = pick_filename("Select a file to remove")
                if filename in selected_files:
                    selected_files.remove(filename)

            # STOP
            elif choice in ("s", "stop", ""):
                break

            else:
                print("Invalid choice.")

        # Store as a simple string (easy to persist)
        return str(selected_files)

    def resolve_helper(self, resolve_params):
        """
        If the source filename is in the skip list, generate a unique path.
        Otherwise, overwrite.
        """

        skip_files = ast.literal_eval(resolve_params.config_value)

        if resolve_params.src_filename in skip_files:
            return True

        return False
