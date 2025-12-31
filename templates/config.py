import os
from utils.config_utils import get_config, overwrite_config
from singleton import Singleton
from typing import final

class Config(Singleton):
    def __init__(self):
        self.config_key = self.__class__.__name__
    
    def resolve(self, source_file_name, prov_dst_dir):
        config = get_config()
        if self.config_key not in config:
            config[self.config_key] = self.prompt_config()
            overwrite_config(config)
        return self.resolve_helper(source_file_name, prov_dst_dir, config[self.config_key])
    def get_config_value(self):
        config = get_config()
        return config[self.config_key]
    
    def clear(self):
        config = get_config()
        del config[self.config_key]
        overwrite_config(config)

    # Asks the user for the config value and return it
    def prompt_config(self):
        raise Exception("This function must be overriden")

    # Returns the same provisional destination directory with or without additional subfolders/subfiles
    def resolve_helper(self, source_file_name, prov_dst_dir, config_value):   
        raise Exception("This function must be overriden")
