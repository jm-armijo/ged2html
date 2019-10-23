import datetime
from src.date import Date
from src.html_element import HTMLElement

class DateRange():
    def __init__(self):
        self.start = Date()
        self.end = Date()

    def is_empty(self):
        return self.start.is_empty() or self.end.is_empty()

    def to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'person-date')
        element.add_attribute('title', self.get_as_yyyymmdd())
        element.set_value(self.get_year_as_text())
        return str(element)

    def get_as_yyyymmdd(self):
        start = self.start.get_as_yyyymmdd()
        end = self.end.get_as_yyyymmdd()
        return "{}/{}".format(start, end)

    def get_year_as_text(self):
        start = self.start.get_year_as_text()
        end = self.end.get_year_as_text()

        if start == end:
            return end
        else:
            return "{}/{}".format(start, end)

    def get_as_text(self):
        return "between " + self.start.get_as_text() + " and " + self.end.get_as_text()

    def __lt__(self, other):
        return self.end < other
