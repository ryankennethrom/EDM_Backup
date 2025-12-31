SOURCE_CONFIGS = []

def register(cls):
    global SOURCE_CONFIGS 
    SOURCE_CONFIGS.append(cls)
    return cls

def load_registry():
    global SOURCE_CONFIGS 
    # Import your name config classes here. Order matters.
    from . import source_config
    from . import add_sources_config

    instantiated = []
    for config in SOURCE_CONFIGS:
        instantiated.append(config())
    SOURCE_CONFIGS = instantiated

load_registry()
