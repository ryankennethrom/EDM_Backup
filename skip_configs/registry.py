SKIP_CONFIGS = []

def register(cls):
    global SKIP_CONFIGS 
    SKIP_CONFIGS.append(cls)
    return cls

def load_registry():
    global SKIP_CONFIGS 
    # Import your name config classes here. Order matters.
    from . import skip_files_config

    instantiated = []
    for config in SKIP_CONFIGS:
        instantiated.append(config())
    SKIP_CONFIGS = instantiated

load_registry()
