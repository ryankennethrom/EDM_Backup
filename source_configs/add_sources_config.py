from templates import Config
from .registry import register
from utils.dir_utils import pick_folder
import ast
import os
import textoutputcontroller as toc


@register
class AdditionalSourcesConfig(Config):

    def prompt(self, prev_config_value):
        """
        Interactive interface for managing a list of source directories.
        """
        selected_dirs = (
            ast.literal_eval(prev_config_value)
            if prev_config_value is not None
            else []
        )

        while True:
            print("\nCurrent additional source folders:")
            if selected_dirs:
                for i, d in enumerate(selected_dirs, 1):
                    print(f"  {i}. {d}")
            else:
                print("  (none)")

            print("\nChoose an action:")
            print("  [A] Add a folder")
            print("  [D] Remove a folder")
            print("  [S] Save & Stop")

            choice = input("> ").strip().lower()

            # ADD FOLDER
            if choice in ("a", "add"):
                folder = pick_folder("Select a folder to add")
                if not folder:
                    continue

                if not os.path.isdir(folder):
                    print("Selected path is not a directory.")
                    continue

                if folder in selected_dirs:
                    print("Folder already added.")
                    continue

                selected_dirs.append(folder)

            # DELETE FOLDER (BY NUMBER)
            elif choice in ("d", "delete"):
                if not selected_dirs:
                    print("No folders to delete.")
                    continue

                try:
                    idx = input("Enter the number of the folder to remove: ").strip()
                    if not idx:
                        continue

                    index = int(idx) - 1

                    if index < 0 or index >= len(selected_dirs):
                        print("Invalid selection.")
                        continue

                    removed = selected_dirs.pop(index)
                    print(f"Removed: {removed}")

                except ValueError:
                    print("Please enter a valid number.")

            # STOP
            elif choice in ("s", "stop", ""):
                break

            else:
                print("Invalid choice.")

        # Store as string for config persistence
        return str(selected_dirs)

    def resolve_helper(self, resolve_params):
        sources = ast.literal_eval(self.config_value)

        for src in sources:
            if not os.path.isdir(src):
                toc.error(
                    f"The source '{src}' does not exist. "
                    "Did your folder structure change? Please replace or remove it."
                )
                self.load_prompt_and_save()
                self.resolve_helper(resolve_params)
                break

        return ast.literal_eval(self.config_value)
