from src.html_element import HTMLElement

class Source():
    def __init__(self, id):
        self.id = id
        self.objects = list()

    def add_object(self, object):
        self.objects.append(object)

    def to_html(self):
        title = self._source_title_to_html()
        content = self._source_content_to_html()

        element = HTMLElement('div')
        element.add_attribute('class', 'source')
        element.set_value(title + content)

        return str(element)

    def _source_title_to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'source-title')
        element.set_value(self.id)

        return str(element)

    def _source_content_to_html(self):
        html = ''
        for object in self.objects:
            content = HTMLElement('img')
            content.add_attribute('class', 'source')
            content.add_attribute('src', "../{}".format(object.file))

            html += str(content)

        element = HTMLElement('div')
        element.add_attribute('class', 'source-content')
        element.set_value(html)

        return str(element)
