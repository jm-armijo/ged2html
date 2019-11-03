class HTMLElement():
    def __init__(self, tag, value=None):
        self.tag = tag
        self.attributes = dict()
        self.value = value

    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        str = '<{}'.format(self.tag)

        for key, value in self.attributes.items():
            str += ' {}="{}"'.format(key, value)

        if self.tag == 'script' and self.value is None:
            self.value = ''

        if self.value is not None:
            str += '>'
            str += self.value
            str += '</{}>'.format(self.tag)
        else:
            str += '/>'

        return str
