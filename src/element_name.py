import re
from src.element import Element

class Name(Element):
    def __init__(self, name):
        super().__init__()

        self.name = name
        parts = self._split_name()
        self.set_given_name(parts[0])
        self.set_last_name(parts[1])

    def set_given_name(self, given_name):
        self.given_name = given_name.lower().replace(',', '')

    def set_last_name(self, last_name):
        self.last_name = last_name.lower().replace(',', '')

    def get_full(self):
        if self.last_name == '' and self.given_name == '':
            return ''
        return "{}, {}".format(self.last_name, self.given_name)

    def _split_name(self):
        match1 = re.search(r'^(.*?)/(.*?)/?\s*$', self.name)
        match2 = re.search(r'^(.*?)/?\s*$', self.name)

        if match1:
            return (match1.group(1).strip(), match1.group(2).strip())
        elif match2:
            return ('', match2.group(1).strip())
