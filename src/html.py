from src.html_element import HTMLElement

class HTMLGenerator():
    def __init__(self, file_name):
        self.file_name = file_name

    def generate(self, title, tree):
        head = self._get_head(title)
        body = self._get_body(title, tree)
        html = self._get_html(head, body)

        file_handler = open(self.file_name, 'w')
        file_handler.write(html)
        file_handler.close()

    @staticmethod
    def wrap_instance(instance, value, attribute_id=''):
        class_name = type(instance).__name__.lower()
        return HTMLGenerator.wrap(class_name, value, attribute_id)

    @staticmethod
    def wrap(class_name, value, attribute_id=''):
        element = HTMLElement('div')
        element.add_attribute('class', class_name)
        element.set_value(value)

        if attribute_id != '':
            element.add_attribute('id', attribute_id)

        return str(element)

    @staticmethod
    def list_to_html(items):
        html = ''
        for item in items:
            html += item.to_html()
        return html

    @staticmethod
    def get_on_load_script(script):
        return (
            '  <script>\n'
            '    window.addEventListener(\n'
            '      "load",\n'
            '      function() {{\n'
            '        "use strict";\n'
            '{}'
            '      }}\n'
            '    );\n'
            '  </script>'
        ).format(script)

    def _get_html(self, head, body):
        return (
            '<!doctype html>\n'
            '<html lang="en">\n'
            '{}\n'
            '{}\n'
            '</html>'
        ).format(head, body)

    def _get_head(self, title):
        return (
            '  <head>\n'
            '    <meta charset="utf-8">\n'
            '    <title>{}</title>\n'
            '    <link href="https://fonts.googleapis.com/css?family=New Rocker" rel="stylesheet">'
            '    <link rel="stylesheet" href="css/styles.css">\n'
            '    <script src="scripts/leader-line.min.js"></script>\n'
            '  </head>'
        ).format(title)

    def _get_body(self, title, body):
        return (
            '<body>\n'
            '<div class="title"><h1>{}</h1>\n'
            '<h2>Family Tree</h2></div>\n'
            '{}\n'
            '</body>'
        ).format(title, body)
