import datetime
from src.date import Date
from src.html_element import HTMLElement

class DateRange():
    def __init__(self):
        self.start = Date()
        self.end = Date()

    def to_html(self):
        separator = HTMLElement('div')
        separator.add_attribute('class', 'separator')
        separator.set_value('&ndash;')

        html = self.start.to_html()
        html += str(separator)
        html += self.end.to_html()

        return html

    def __str__(self):
        str = ''
        if not self.end.is_empty() or (not self.start.is_empty() and int(self.start.year) < datetime.datetime.now().year - 100):
            str = "{} - {}".format(self.start.year, self.end.year)

        return str
