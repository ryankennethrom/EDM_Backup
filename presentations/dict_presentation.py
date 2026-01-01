from singleton import Singleton
from data_classes import DictionaryPresentationParameters

class DictPresentation(Singleton):
    def present(self, dict_pre_params):
        # Type check
        if not isinstance(dict_pre_params, DictPresentationParameters):
            raise Exception("Pass the right data class for this function")

        # Extract attributes
        items = dict_pre_params.string_dict     # dictionary
        indentation = dict_pre_params.indentation
        connector = dict_pre_params.connector   # e.g., ": "
        ordering = dict_pre_params.ordering     # Ordering enum

        indent = ' ' * indentation

        for i, (key, value) in enumerate(items.items(), start=1):
            if ordering == Ordering.NUMBERED:
                print(f"{indent}{i}. {key}{connector}{value}")
            else:
                raise Exception(f"Unknown ordering: {ordering}")
