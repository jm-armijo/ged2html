import re
from src.html import HTMLGenerator
from src.node import Node

# pylint: disable=too-many-instance-attributes
class Person(Node):
    def __init__(self, person_id=''):
        super().__init__()

        self.id = person_id
        self.given_name = ''
        self.last_name = ''
        self.sex = ''
        self.birth_date = ''
        self.birth_place = ''
        self.death_date = ''
        self.death_place = ''
        self.unions = list()

    def set_name(self, name):
        name_parts = self._split_name(name)
        self.set_given_name(name_parts[0])
        self.last_name = name_parts[1].lower()

    def set_given_name(self, given_name):
        if self.given_name == '':
            self.given_name = given_name.lower()

    def set_sex(self, sex):
        self.sex = sex

    def set_birth_date(self, date):
        self.birth_date = date

    def set_birth_place(self, place):
        self.birth_place = place

    def set_death_date(self, date):
        self.death_date = date

    def set_death_place(self, place):
        self.death_place = place

    def set_parents(self, parents):
        self.parents.append(parents)

    def add_union(self, union):
        self.unions.append(union)
        self.children += union.get_children()

    def get_spouses(self):
        return [self]

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents

    def get_unions(self):
        return self.unions

    def is_single(self):
        return len(self.unions) == 0

    def to_html(self):
        value = (
            '  <div class="photo"><img class="photo" src="images/face.png"></div>\n'
            '  <div class="given">{}</div>\n'
            '  <div class="last">{}</div>\n'
            '  <div class="dates">{} - {}</div>\n'
        ).format(
            self.given_name,
            self.last_name,
            self.birth_date,
            self.death_date
        )

        return HTMLGenerator.wrap(self, value, self.id)

    # pylint: disable=no-self-use
    def _split_name(self, name):
        match = re.search(r'^(.*?)/(.*?)/?\s*$', name)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        else:
            print("Unable to get first and last name from '{}'".format(name))
            return ('', '')

    def __str__(self):
        return "[{} {}]".format(self.given_name, self.last_name)
