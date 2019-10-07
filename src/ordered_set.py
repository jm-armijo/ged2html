class OrderedSet():
    def __init__(self, values=None):
        self.values = list()
        if values is not None:
            self.append_list(values)

    def append_list(self, values):
        for value in values:
            self.append_value(value)

    def append_value(self, value):
        if value not in self.values:
            self.values.append(value)

    def to_list(self):
        return self.values

    def __add__(self, other):
        self.append_list(other.values)

    def __str__(self):
        return str(self.values)

    def __iter__(self):
        for x in list.__iter__(self.values):
            yield x
