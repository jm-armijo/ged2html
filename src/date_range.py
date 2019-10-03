from src.date import Date
from src.html_element import HTMLElement

class DateRange():
    def __init__(self):
        self.start = Date()
        self.end = Date()

    def to_html(self):
        html = self.start.to_html()
        if not self.start.is_empty() or not self.end.is_empty():
            separator = HTMLElement('div')
            separator.add_attribute('class', 'separator')
            separator.set_value('&ndash;')

            html += str(separator)

        html += self.end.to_html()
        return html
