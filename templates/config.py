import os
from utils.config_utils import get_config, overwrite_config
from singleton import Singleton
from typing import final
from data_classes import ResolveParameters

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

    def resolve(self, resolve_params):
        if not isinstance(resolve_params, ResolveParameters):
            raise Exception("You must pass a ResolveParameters() object to Config.resolve()")

        self.load_config()
        if self.config_value is None:
            self.config_value = self.prompt(self.config_value)
            if self.config_value is None:
                raise Exception(f"{self.__class__.__name__}.prompt() is returning a value of type None. Make sure prompt() doesn't return None.")
            self.save_config()
        resolve_params.config_value = self.config_value
        return self.resolve_helper(resolve_params)

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
    def resolve_helper(self, resolve_params):   
        raise Exception("This function must be overriden")
