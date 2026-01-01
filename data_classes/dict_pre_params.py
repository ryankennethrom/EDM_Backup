from constants import Ordering

class DictionaryPresentationParameters:
    def __init__(self):
        self.string_dict = dict()
        self.indentation = 0
        self.connector = "-->"
        self.ordering = Ordering.NUMBERED
