import datetime

class Date():

    def __init__(self):
        self.type = ''
        self.day = ''
        self.month = ''
        self.year = ''

    def set_type(self, type):
        self.type = type

    def set_day(self, day):
        self.day = day

    def set_month(self, month):
        self.month = month

    def set_year(self, year):
        self.year = year

    def get_full(self):
        date = self.year
        if (self.month != ''):
            date = self.month + " " + date
            if (self.day != ''):
                date = self.day + " " + date

        return date
