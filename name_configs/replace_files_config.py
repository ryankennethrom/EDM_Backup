class ReplaceFilesConfig():
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

    def resolve(self, source_filename, prov_dst_dir):
        if self.config_value == "true":
            return os.path.join(prov_dst_dir, source_filename)
        else:
            return get_unique_path(prov_dst_dir, source_filename)

