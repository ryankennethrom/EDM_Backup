from templates import Config
from .registry import register
import ast
import os
from datetime import datetime
import textoutputcontroller as toc

@register
class OrganizeByCreatedYearConfig(Config):
    def prompt(self, prev_config_value):
        answer = input("Organize files by year they are created ? [Enter Y/n]: ").strip().lower()
        return answer in ("", "y", "yes")

    def resolve_helper(self, resolve_params):
        if not os.path.isdir(resolve_params.dst_dirpath):
            toc.info(f"Warning: {self.__class__.__name__} encountered the invalid directory: {resolve_params.dst_dirpath}")
            return resolve_params.dst_dirpath

        enabled = (
            resolve_params.config_value
            if isinstance(resolve_params.config_value, bool)
            else ast.literal_eval(resolve_params.config_value)
        )

        if not enabled:
            return resolve_params.dst_dirpath

        created_year = datetime.fromtimestamp(os.path.getctime(resolve_params.src_filepath)).year

        year_dir = os.path.join(resolve_params.dst_dirpath, str(created_year)) 
        
        os.makedirs(year_dir, exist_ok=True)

        return year_dir
