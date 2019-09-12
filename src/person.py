import re
from src.html import HTMLGenerator
from src.node import Node

# pylint: disable=too-many-instance-attributes
class Person(Node):
    def __init__(self, person_id):
        self.id = person_id
        self.given_name = ''
        self.last_name = ''
        self.sex = ''
        self.birth_date = ''
        self.birth_place = ''
        self.death_date = ''
        self.death_place = ''
        self.parents = None
        self.unions = list()

    def set_name(self, name):
        name_parts = self._split_name(name)
        self.set_given_name(name_parts[0])
        self.last_name = name_parts[1]

    def set_given_name(self, given_name):
        if self.given_name == '':
            self.given_name = given_name

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
        self.parents = parents

    def add_union(self, union):
        self.unions.append(union)

    def get_spouses(self):
        return [self]

    def get_children(self):
        children = list()
        for union in self.unions:
            children += union.get_children()
        return children

    def get_parents(self):
        if self.parents is None:
            return list()
        else:
            return [self.parents]

    def get_unions(self):
        return self.unions

    def is_single(self):
        return len(self.unions) == 0

    def to_html(self):
        value = (
            '  <img class="photo" src="images/face.png">\n'
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
