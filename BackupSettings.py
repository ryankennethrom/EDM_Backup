from directory_configs.registry import DIRECTORY_CONFIGS
from name_configs.registry import NAME_CONFIGS
from skip_configs.registry import SKIP_CONFIGS
from source_configs.registry import SOURCE_CONFIGS
from data_classes import *
from presentations import *
import ast
import os

def clear_screen():
    os.system('cls')

def main():
    # Collect all config objects
    configs = SOURCE_CONFIGS + DIRECTORY_CONFIGS + NAME_CONFIGS + SKIP_CONFIGS

    # Map number → config object for menu
    config_map = {str(i + 1): cfg for i, cfg in enumerate(configs)}

    while True:
        print("\n =================== Backup Settings ======================= ")
        for num, cfg in config_map.items():
            # Get current value for display, fallback to empty string if not available
            try:
                raw_value = cfg.get_config_value()
                value = raw_value
            except AttributeError:
                value = "(no value)"
            print(f"  [{num}] {cfg.__class__.__name__.removesuffix("Config")}{"*" if value is None else ""}")
        print("  [X] Exit")

        choice = input("\nSelect a config to reset or X to exit: ").strip().lower()
        clear_screen()

        if choice == "x":
            print("Exiting configuration interface.")
            break

        elif choice in config_map:
            cfg_obj = config_map[choice]
            print("[Current Value]")
            cfg_obj.print_report()
            answer = input("Proceed with the reset ? [Y/n] ")
            clear_screen()
            if answer.lower() in ("y", "yes", "1"):
                print("==> Reset Started. Please answer the following prompts ... ")
                new_value = cfg_obj.load_prompt_and_save()
                clear_screen()
                print("[Updated Value]")
                cfg_obj.print_report()
                input("Press any key to go back to settings (continue) ")
                clear_screen()
            else:
                clear_screen()
        else:
            print("Invalid choice. Enter a number or X to exit.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ran into an error: {e}")
