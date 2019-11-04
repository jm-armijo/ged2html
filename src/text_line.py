import re

# pylint: disable=too-few-public-methods
class TextLine():
    def __init__(self, line):
        self.line = line
        self.parse_line(line)

    def parse_line(self, line):
        id_pattern = re.compile(r"(\d+)\s(@.*@)\s(\w+)(?:\s(.+))?")
        data_pattern = re.compile(r"(\d+)\s(\w*)(?:\s(.+))?")

        if id_pattern.match(line):
            match = id_pattern.search(line)
            self.level = int(match.group(1))
            self.id = match.group(2)
            self.tag = match.group(3)
            self.data = match.group(4)
        elif data_pattern.match(line):
            match = data_pattern.search(line)
            self.level = int(match.group(1))
            self.tag = match.group(2)
            self.data = match.group(3)
        else:
            raise "Cannot process line {}".format(line)

        if self.data is None:
            self.data = ''
