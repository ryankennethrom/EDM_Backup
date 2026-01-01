from templates import Config
from .registry import register
import os

@register
class ReplaceFilesConfig(Config):
    def get_unique_path(self, dst_dir, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        candidate = filename

        while os.path.exists(os.path.join(dst_dir, candidate)):
            candidate = f"{base}({counter}){ext}"
            counter += 1

        return os.path.join(dst_dir, candidate)

    def prompt(self, prev_config_value):
        answer = input(
            "Replace files in destination or keep copies?\n"
            "[Enter R to replace / C to keep copies] "
        ).strip().lower()

        if answer in ("", "r", "replace"):
            return "True"
        else:
            return "False"

    def resolve_helper(self, resolve_params):
        if resolve_params.config_value == "True":
            dst_path = os.path.join(resolve_params.dst_dirpath, resolve_params.src_filename)
            if os.path.isfile(dst_path):
                os.remove(dst_path)
            return dst_path
        else:
            return self.get_unique_path(resolve_params.dst_dirpath, resolve_params.src_filename)

