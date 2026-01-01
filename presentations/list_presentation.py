from singleton import Singleton
from data_classes import ListPresentationParameters

class ListPresentation(Singleton):
    def present(self, lst_pre_params):
        # Type check
        if not isinstance(lst_pre_params, ListPresentationParameters):
            raise Exception("Pass the right data class for this function")
        
        # Extract attributes
        items = lst_pre_params.string_list
        indentation = lst_pre_params.indentation
        ordering = lst_pre_params.ordering  # now an Ordering enum

        indent = ' ' * indentation

        for i, item in enumerate(items, start=1):
            if ordering == Ordering.NUMBERED:
                print(f"{indent}{i}. {item}")
            else:
                raise Exception(f"Unknown ordering: {ordering}")
