import os
import sys

def get_config():
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, "backup.config")

    if not os.path.isfile(config_path):
        return {}

    config = {}

    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key] = value
    return config

def overwrite_config(config):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, "backup.config")

    with open(config_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

