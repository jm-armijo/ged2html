import re
from src.element import Element

class Name(Element):
    def __init__(self, name):
        super().__init__()

        self.name = name
        parts = self._split_name()
        self.given_name = parts[0].lower()
        self.last_name = parts[1].lower()

    def get_full(self):
        return "{}, {}".format(self.last_name, self.given_name)

    def _split_name(self):
        match1 = re.search(r'^(.*?)/(.*?)/?\s*$', self.name)
        match2 = re.search(r'^(.*?)/?\s*$', self.name)

        if match1:
            return (match1.group(1).strip(), match1.group(2).strip())
        elif match2:
            return ('', match2.group(1).strip())
