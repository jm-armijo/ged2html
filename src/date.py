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

    def get_full(self):
        date = self.year
        if self.month != '':
            date = self.month + " " + date
            if self.day != '':
                date = self.day + " " + date

        return date
