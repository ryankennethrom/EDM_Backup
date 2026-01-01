from directory_configs.registry import DIRECTORY_CONFIGS
from name_configs.registry import NAME_CONFIGS
from skip_configs.registry import SKIP_CONFIGS
from source_configs.registry import SOURCE_CONFIGS
from data_classes import *
from presentations import *
import ast

def main():
    # Collect all config objects
    configs = SOURCE_CONFIGS + DIRECTORY_CONFIGS + NAME_CONFIGS + SKIP_CONFIGS

    # Map number → config object for menu
    config_map = {str(i + 1): cfg for i, cfg in enumerate(configs)}

    while True:
        print("\n=== Configuration Interface ===")
        for num, cfg in config_map.items():
            # Get current value for display, fallback to empty string if not available
            try:
                raw_value = cfg.get_config_value()
                value = raw_value
            except AttributeError:
                value = "(no value)"
            if isinstance(value, list):
                params = ListPresentationParameters()
                params.string_list = value
                print(f"  [{num}] {cfg.__class__.__name__}:")
                ListPresentation.present(params)
            elif isinstance(value, dict):
                params = DictionaryPresentationParameters()
                params.string_dict = value
                print(f"  [{num}] {cfg.__class__.__name__}:")
                DictionaryPresentation.present(params)
            else:
                print(f"  [{num}] {cfg.__class__.__name__}: {value}")
        print("  [X] Exit")

        choice = input("\nSelect a config to reset or X to exit: ").strip().lower()

        if choice == "x":
            print("Exiting configuration interface.")
            break

        elif choice in config_map:
            cfg_obj = config_map[choice]
            print(f"\n--- Resetting {cfg_obj.__class__.__name__} ---")
            new_value = cfg_obj.load_prompt_and_save()
            print(f"\nUpdated config for {cfg_obj.__class__.__name__}: {new_value}\n")

        else:
            print("Invalid choice. Enter a number or X to exit.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Config Interface Error: {e}")
