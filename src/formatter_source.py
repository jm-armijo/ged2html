from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class SourceFormatter():
    def __init__(self, source):
        self.source = source

    def format(self):
        title = self._source_title_to_html()
        content = self._source_content_to_html()

        element = HTMLElement('div')
        element.add_attribute('class', 'source')
        element.set_value(title + content)

        return str(element)

    def _source_title_to_html(self):
        title = HTMLElement('div')
        title.add_attribute('class', 'table-title')
        title.add_attribute('id', self.source.id)
        title.set_value(self.source.title)

        element = HTMLElement('div')
        element.add_attribute('class', 'table-header')
        element.set_value(str(title))

        return str(element)

    def _source_content_to_html(self):
        html = ''
        for object in self.source.objects:
            html += self._object_to_html(object)

        element = HTMLElement('div')
        element.add_attribute('class', 'source-content')
        element.set_value(html)

        return str(element)

    def _object_to_html(self, object):
        path_to_image = "../{}".format(object.file)

        content = HTMLElement('img')
        content.add_attribute('class', 'source')
        content.add_attribute('src', path_to_image)

        link = HTMLElement('a')
        link.add_attribute('href', path_to_image)
        link.add_attribute('target', '_blank')
        link.set_value(str(content))

        return str(link)

FormatterFactory.register('Source', SourceFormatter)
