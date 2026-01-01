from templates import Config
from .registry import register
import ast
import os
from datetime import datetime
import textoutputcontroller as toc

@register
class OrganizeByCurrentYearConfig(Config):
    def prompt(self, prev_config_value):
        answer = input("Organize files by current year? [Enter Y/n]: ").strip().lower()
        return answer in ("", "y", "yes")

    def resolve_helper(self, resolve_params):
        if not os.path.isdir(resolve_params.dst_dirpath):
            toc.info(f"Warning: {self.__class__.__name__} encounted the invalid directory: {resolve_params.dst_dirpath}")
            return resolve_params.dst_dirpath

        enabled = (
            resolve_params.config_value
            if isinstance(resolve_params.config_value, bool)
            else ast.literal_eval(resolve_params.config_value)
        )

        if not enabled:
            return resolve_params.dst_dirpath

        year_dir = os.path.join(resolve_params.dst_dirpath, str(datetime.now().year))

        os.makedirs(year_dir, exist_ok=True)
        return year_dir
