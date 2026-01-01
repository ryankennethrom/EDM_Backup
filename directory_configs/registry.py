DIRECTORY_CONFIGS = []

def register(cls):
    global DIRECTORY_CONFIGS

    DIRECTORY_CONFIGS.append(cls)
    return cls

def load_registry():
    global DIRECTORY_CONFIGS

    from . import prefix_destination_config 
    from . import default_destination_config
    from . import org_by_curr_year_config
    from . import created_year_org_config

    
    instantiated = []
    for config in DIRECTORY_CONFIGS:
        instantiated.append(config())
    DIRECTORY_CONFIGS = instantiated

load_registry()
