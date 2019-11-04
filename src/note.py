class Note():
    def __init__(self, id):
        self.id = id
        self.value = list()

    def add_value(self, value):
        if value != '':
            self.value.append(value)

    def concatenate_value(self, value):
        if value != '':
            self.value[-1] += value
