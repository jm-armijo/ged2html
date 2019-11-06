from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class SourceFormatter():
    def __init__(self, source):
        self.source = source

    def format(self):
        separator = HTMLElement('div', ',')
        separator.add_attribute('class', 'source-separator')
        separator = str(separator)

        objects = self.source.objects
        formatted_objects = list()

        for i in range(len(objects)):
            object = objects[i]
            title = self.get_title(i, len(objects))
            formatted_objects.append(self.format_object(object, title))

        return separator.join(formatted_objects)

    def get_title(self, index, length):
        if length == 1:
            return "{}".format(self.source.title)
        else:
            return "{} ({}/{})".format(self.source.title, index+1, length)

    def format_object(self, object, title):
        path_to_image = "../{}".format(object.file.path)
        link = HTMLElement('a')
        link.add_attribute('href', path_to_image)
        link.add_attribute('target', '_blank')
        link.set_value(title)

        return str(link)

FormatterFactory.register('Source', SourceFormatter)
