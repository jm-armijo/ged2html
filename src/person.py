import datetime
import re

from src.date import Date
from src.node import Node

from src.element_name import Name
from src.element_event import Event

# pylint: disable=too-many-instance-attributes
class Person(Node):
    def __init__(self, person_id=''):
        super().__init__()

        self.id = person_id
        self.name = Name('')
        self.birth = Event()
        self.baptism = Event()
        self.death = Event()
        self.burial = Event()
        self.nationality = Event()
        self.occupation = Event()

        self.gender = 'U'
        self.unions = list()
        self.objects = list()
        self.notes = list()
        self.private = False

    def can_show_dates(self):
        limit = Date()
        limit.set_year(datetime.datetime.now().year - 99)

        if not self.death.date.is_empty() or (not self.birth.date.is_empty() and self.birth.date < limit):
            return True
        else:
            return False

    def set_given_name(self, given_name):
        self.name.given_name = given_name.lower()

    def set_last_name(self, last_name):
        self.name.last_name = last_name.lower()

    def is_private(self):
        return self.private

    def set_death_date(self, date):
        self.death_date = date

    def set_death_place(self, place):
        self.death_place = place

    def set_parents(self, parents):
        self.parents.append(parents)

    def add_union(self, union):
        self.unions.append(union)
        self.children += union.get_children()

    def add_object(self, object_id):
        self.objects.append(object_id)

    def add_note(self, note_id):
        self.notes.append(note_id)

    def get_full_name(self):
        return self.name.get_full()

    def get_given_name(self):
        return self.name.given_name

    def get_last_name(self):
        return self.name.last_name

    def get_spouses(self):
        return [self]

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents

    def get_unions(self):
        return self.unions

    def get_sources(self):
        sources = self.birth.sources
        sources += self.death.sources

        for union in self.unions:
            sources += union.get_sources()
        return sources

    def is_single(self):
        return len(self.unions) == 0

    # pylint: disable=no-self-use
    def _split_name(self, name):
        match = re.search(r'^(.*?)/(.*?)/?\s*$', name)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        else:
            match = re.search(r'^(.*?)/?\s*$', name)
            return ('', match.group(1).strip())

    def __contains__(self, item):
        return item == self
