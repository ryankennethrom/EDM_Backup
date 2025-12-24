NAME_CONFIGS = []

def register(cls):
    global NAME_CONFIGS 
    NAME_CONFIGS.append(cls)
    return cls

def load_registry():
    global NAME_CONFIGS 
    # Import your name config classes here. Order matters.
    from . import replace_files_config

    instantiated = []
    for config in NAME_CONFIGS:
        instantiated.append(config())
    NAME_CONFIGS = instantiated

load_registry()
