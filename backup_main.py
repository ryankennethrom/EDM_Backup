from directory_configs.registry import DIRECTORY_CONFIGS
from name_configs.registry import NAME_CONFIGS
from source_config import SOURCE_CONFIG
import os
import shutil
import textoutputcontroller as toc

if __name__ == "__main__":
    try:
        src = SOURCE_CONFIG().get_save_return()
        src_filenames = os.listdir(src) 
        
        toc.info(f"Backing up files from {src}")
        
        count = 0
        for name in src_filenames:
            src_path = os.path.abspath(os.path.join(src, name))
            
            toc.info(f"Backing up {src_path}")
            
            dst_path = ""

            toc.info(f"Resolving directory")
            
            to_log = "No Path"
            for dir_config in DIRECTORY_CONFIGS:
                to_log += f" ==={dir_config.__class__.__name__}"
                resolved_dst = dir_config.resolve(name, dst_path)
                if not resolved_dst.startswith(dst_path):
                    raise Exception(
                            f"One of your directory configs is overwriting previous config's changes."
                            "Make sure your directory configs are imported in the right order."
                            f"Config Name: {dir_config.__class__.__name__}"
                            f"Input path: {dst_path}"
                            f"Output path: {resolved_dst}\n"
                    )
                dst_path = resolved_dst
                to_log += f"===> {dst_path}"
            
            toc.info(to_log)

            toc.info(f"Resolving filename")
            
            to_log = dst_path
            for name_config in NAME_CONFIGS:
                to_log += f" ==={name_config.__class__.__name__}"
                name_resolved_dst = name_config.resolve(name, dst_path)
                if not name_resolved_dst.startswith(dst_path):
                    raise Exception(
                            f"One of your name configs is overwriting previous config's changes."
                            f"Config Name: {name_config.__class__.__name__}"
                            f"Input path: {dst_path}"
                            f"Output path: {named_resolved_dst}"
                    )
                dst_path = name_resolved_dst
                to_log += f"===> {dst_path}"
            
            toc.info(to_log)

            toc.info(f"Backing up from {src_path} to {dst_path}") 
            shutil.move(src_path, dst_path)
            count += 1
        toc.info(f"Backed up a total of {count} files")
    except Exception as e:
        toc.error(f"Error occured : {e}")


