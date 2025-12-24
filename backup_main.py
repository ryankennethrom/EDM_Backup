from source import SOURCE
from path_resolvers import __all__ as modules



if __name__ == "__main__":
    src = SOURCE().get()
    for name in os.listdir(src):
        src_path = os.path.abspath(os.path.join(src, name))
        dst = ""

        for resolver in get_path_resolvers():
            path_resolved_dst = resolver.resolve(name, dst)
            if not path_resolved_dst.startswith(dst):
                raise Exception(f"Your path resolver classes order may be wrong. \n Previous Path: {dst} \n Resolved Path: {resolved_dst}\n")
            dst = path_resolved_dst
        
        name_resolved_dst = dst
        for resolver in get_name_resolvers():
            name_resolved_dst = resolver.resolve(name, name_resolved_dst)
            if not name_resolved_dst.startswith(dst):
                raise Exception(f"One of your name resolvers is changing destination directory."
        dst = name_resolved_dst


