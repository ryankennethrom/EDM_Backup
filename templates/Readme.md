# How to add new templates

Create your example template class in this directory and add the following to templates/__init__.py : 

from .example import ExampleClass # add this

__all__ = [
    "ExampleClass" # add this
]
