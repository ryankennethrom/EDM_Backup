from templates import Config
from .registry import register
from utils.dir_utils import pick_filename
import os


@register
class SkipFilesConfig(Config):

    def prompt_config(self):
        """
        Interactive interface for managing a list of filenames.
        """
        selected_files = []

        while True:
            print("\nFiles to be skipped :")
            if selected_files:
                for i, f in enumerate(selected_files, 1):
                    print(f"  {i}. {f}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a file to skip")
            print("  [D] Remove file ")
            print("  [S] Stop")

            choice = input("> ").strip().lower()

            # ADD FILE
            if choice in ("a", "add"):
                filename = pick_filename("Select a file to add")
                if filename and filename not in selected_files:
                    selected_files.append(filename)

            # DELETE FILE
            elif choice in ("d", "delete"):
                if not selected_files:
                    print("No files to delete.")
                    continue

                filename = pick_filename("Select a file to delete")
                if filename in selected_files:
                    selected_files.remove(filename)

            # STOP
            elif choice in ("s", "stop", ""):
                break

            else:
                print("Invalid choice.")

        # Store as a simple string (easy to persist)
        return ",".join(selected_files)

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        """
        If the source filename is in the skip list, generate a unique path.
        Otherwise, overwrite.
        """
        skip_files = set(
            f for f in config_value.split(",") if f
        )

        if source_filename in skip_files:
            return False

        return True
