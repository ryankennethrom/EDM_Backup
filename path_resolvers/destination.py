from config_utils import get_cofig, overwrite_config
class DESTINATION:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self):
        config = get_config()
        if "DESTINATION" not in config or not os.path.isdir(config["DESTINATION"]):
            answer = input(
                "Script doesn't know where to back up files.\n"
                "Assign destination folder? [Enter Y/n]: "
            ).strip().lower()

            if answer in ("", "y", "yes"):
                dst = pick_folder("Select folder to store backed up files")

                if not dst:
                    raise SystemExit("No destination folder selected. Exiting.")

            else:
                raise SystemExit("Destination folder not set. Exiting.")

            config["DESTINATION"] = dst
            overwrite_config(config)
        return config['DESTINATION']

