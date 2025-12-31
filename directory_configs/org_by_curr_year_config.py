from templates import Config
from .registry import register
import ast
import os
from datetime import datetime


@register
class OrganizeByCurrentYearConfig(Config):
    def prompt(self, prev_config_value):
        answer = input("Organize files by current year? [Enter Y/n]: ").strip().lower()
        return answer in ("", "y", "yes")

    def resolve_helper(self, source_filename, source_filepath, prov_dst_dir, config_value):
        enabled = (
            config_value
            if isinstance(config_value, bool)
            else ast.literal_eval(config_value)
        )

        if not enabled:
            return prov_dst_dir

        year_dir = os.path.join(prov_dst_dir, str(datetime.now().year))

        # ✅ CRITICAL FIX
        os.makedirs(year_dir, exist_ok=True)

        return year_dir
