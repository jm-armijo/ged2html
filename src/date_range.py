import datetime
from src.date import Date
from src.html_element import HTMLElement

class DateRange():
    def __init__(self):
        self.start = Date()
        self.end = Date()

    def is_empty(self):
        return self.start.is_empty() or self.end.is_empty()

    def get_year(self):
        return min(self.start.year, self.end.year)

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
