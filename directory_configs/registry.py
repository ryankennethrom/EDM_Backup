DIRECTORY_CONFIGS = []

def register(cls):
    global DIRECTORY_CONFIGS

    DIRECTORY_CONFIGS.append(cls)
    return cls

def load_registry():
    global DIRECTORY_CONFIGS

    # Import your resolvers here. Order matters.
    from . import prefix_destination_config 
    from . import default_destination_config

    
    instantiated = []
    for config in DIRECTORY_CONFIGS:
        instantiated.append(config())
    DIRECTORY_CONFIGS = instantiated

load_registry()
