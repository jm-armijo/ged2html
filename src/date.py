from src.html_element import HTMLElement

class Date():

    def __init__(self):
        self.precision = ''
        self.day = ''
        self.month = ''
        self.year = ''

    def is_empty(self):
        return self.year == ''

    def set_precision(self, precision):
        self.precision = precision

    def set_day(self, day):
        self.day = day

    def set_month(self, month):
        self.month = month

    def set_year(self, year):
        self.year = year

    def to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'person-date')
        element.add_attribute('title', self._get_full())
        element.set_value(self.year)
        return str(element)

    def _get_full(self):
        date = self.year
        if self.month != '':
            date = self.month + " " + date
            if self.day != '':
                date = self.day + " " + date

        return date
