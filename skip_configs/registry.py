SKIP_CONFIGS = []

def register(cls):
    global SKIP_CONFIGS 
    SKIP_CONFIGS.append(cls)
    return cls

def load_registry():
    global SKIP_CONFIGS 
    
    # Import your skip config classes between the START and END markers. Order may matter depending on individual class's implementations.
    # START

    from . import skip_file_names_config
    from . import skip_folder_names_config

    # END

    # Guardrails. Recommended not to move.
    from . import skip_undefined_destinations
    from . import skip_nonexistent_destinations
    
    instantiated = []
    for config in SKIP_CONFIGS:
        instantiated.append(config())
    SKIP_CONFIGS = instantiated

load_registry()
