import os
from utils.config_utils import get_config, overwrite_config
from singleton import Singleton
from typing import final

class Config(Singleton):
    def __init__(self):
        self.config_key = self.__class__.__name__
        self.config_value = None

    def load_config(self):
        config = get_config()
        self.config_value = (config[self.config_key] if self.config_key in config else None)

    def save_config(self):
        config = get_config()
        config[self.config_key] = self.config_value
        overwrite_config(config)

    def resolve(self, source_file_name, source_file_path, prov_dst_dir):
        self.load_config()
        if self.config_value is None:
            self.config_value = self.prompt(self.config_value)
            self.save_config()
        return self.resolve_helper(source_file_name, source_file_path, prov_dst_dir, self.config_value)

    def get_config_value(self):
        self.load_config()
        return self.config_value
    
    def load_prompt_and_save(self):
        self.load_config()
        new_config_value = self.prompt(self.config_value)
        self.config_value = new_config_value
        self.save_config()

    def prompt(self, prev_config_value):
        raise Exception("This function must be overriden")

    # Returns the same provisional destination directory with or without additional subfolders/subfiles
    def resolve_helper(self, source_file_name, source_file_path, prov_dst_dir, config_value):   
        raise Exception("This function must be overriden")
