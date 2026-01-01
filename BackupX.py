import textoutputcontroller as toc
from data_classes import ResolveParameters
from directory_configs.registry import DIRECTORY_CONFIGS        
from name_configs.registry import NAME_CONFIGS
from skip_configs.registry import SKIP_CONFIGS
from source_configs.registry import SOURCE_CONFIGS
import os
import shutil

def isFileSkip(resolve_params):
    toc.info(f"Resolving file inclusion")
    for config in SKIP_CONFIGS:
        if config.resolve(resolve_params) == True:
            toc.info(f"Skipping {resolve_params.src_filename} because of {config.__class__.__name__}")
            return True
    return False


if __name__ == "__main__":
    try:
        sources = []
        for config in SOURCE_CONFIGS:
            params = ResolveParameters()
            new_srcs = config.resolve(params)            
            sources += new_srcs

        
        for src in sources:

            src_filenames = os.listdir(src) 
            
            toc.info(f"Backing up files from {src}")
            
            count = 0
            for name in src_filenames:
                src_path = os.path.abspath(os.path.join(src, name))
                
                toc.info(f"Backing up {src_path}")
                
                dst_path = ""

                toc.info(f"Resolving directory")
                
                to_log = ""
                for dir_config in DIRECTORY_CONFIGS:
                    to_log += f" ==={dir_config.__class__.__name__}"
                    
                    params = ResolveParameters()
                    params.src_filename = name
                    params.src_filepath = src_path
                    params.dst_dirpath = dst_path

                    resolved_dst = dir_config.resolve(params)
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

                dir_path = dst_path

                toc.info(f"Resolving filename")
                
                to_log = dst_path
                for name_config in NAME_CONFIGS:
                    to_log += f" ==={name_config.__class__.__name__}"

                    params = ResolveParameters()
                    params.src_filename = name
                    params.src_filepath = src_path
                    params.dst_dirpath = dst_path

                    name_resolved_dst = name_config.resolve(params)
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

                params = ResolveParameters()
                params.src_filename = name
                params.src_filepath = src_path
                params.dst_dirpath = dir_path
                params.dst_filepath = dst_path

                if isFileSkip(params):
                    continue

                toc.info(f"Backing up from {src_path} to {dst_path}") 
                shutil.move(src_path, dst_path)
                count += 1
            toc.info(f"Backed up a total of {count} files for the source {src}")
    except Exception as e:
        toc.error(f"Error occured : {e}")


