from src.html_element import HTMLElement

class Date():

    def __init__(self):
        self.precision = ''
        self.day = ''
        self.month = ''
        self.year = ''
        self.time = ''

    def set_precision(self, precision):
        self.precision = precision

    def set_day(self, day):
        self.day = day

    def set_month(self, month):
        self.month = month

    def set_year(self, year):
        self.year = year

    def is_empty(self):
        return self.year == ''

    def get_as_yyyymmdd(self):
        value = self.year
        if self.month:
            value += "-{}".format(self.month)
            if self.day:
                value += "-{}".format(self.day)
        return value

    def get_year_as_text(self):
        return self.year

    def get_as_text(self):
        date = self.year
        if self.month != '':
            date = self.month + " " + date
            if self.day != '':
                date = self.day + " " + date

        return date

    def __lt__(self, other):
        return int(self.year) < other.year
