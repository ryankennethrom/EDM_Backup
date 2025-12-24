from templates import BackupPathConfig
from .registry import register
import os

@register
class ReplaceFilesConfig(BackupPathConfig):
    def get_unique_path(self, dst_dir, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        candidate = filename

        while os.path.exists(os.path.join(dst_dir, candidate)):
            candidate = f"{base}({counter}){ext}"
            counter += 1

        return os.path.join(dst_dir, candidate)

    def prompt_config(self):
        answer = input(
            "Replace files in destination or keep copies?\n"
            "[Enter R to replace / C to keep copies] "
        ).strip().lower()

        if answer in ("", "r", "replace"):
            return "true"
        else:
            return "false"

    def resolve_helper(self, source_filename, prov_dst_dir, config_value):
        if config_value == "true":
            dst_path = os.path.join(prov_dst_dir, source_filename)
            if os.path.isfile(dst_path):
                os.remove(dst_path)
            return dst_path
        else:
            return self.get_unique_path(prov_dst_dir, source_filename)

