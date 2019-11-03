import sys, traceback

class FormatterFactory():
    registry = dict()

    def make(object):
        formatable_class_name = object.__class__.__name__
        formatter_class = FormatterFactory.registry[formatable_class_name]
        return formatter_class(object)

    def register(formatable_class_name, formatter_class):
        FormatterFactory.registry[formatable_class_name] = formatter_class
