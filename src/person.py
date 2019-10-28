import datetime
import re
from src.date_range import DateRange
from src.date import Date
from src.html_element import HTMLElement
from src.node import Node

# pylint: disable=too-many-instance-attributes
class Person(Node):
    def __init__(self, person_id=''):
        super().__init__()

        self.id = person_id
        self.first_name = ''
        self.last_name = ''
        self.sex = 'U'
        self.birth_date = Date()
        self.death_date = Date()
        self.birth_place = ''
        self.death_place = ''
        self.unions = list()
        self.objects = list()
        self.sources = list()
        self.private = False

    def get_pronoun(self):
        if self.sex == 'M':
            return 'he'
        elif self.sex == 'F':
            return 'she'
        else:
            return 'they'

    def can_show_dates(self):
        limit = Date()
        limit.set_year(datetime.datetime.now().year - 99)

        if not self.death_date.is_empty() or (not self.birth_date.is_empty() and self.birth_date < limit):
            return True
        else:
            return False

    def get_birth_date(self):
        if self.can_show_dates():
            return self.birth_date
        else:
            return Date()

    def get_death_date(self):
        if self.can_show_dates():
            return self.death_date
        else:
            return Date()

    def set_name(self, name):
        name_parts = self._split_name(name)
        self.set_given_name(name_parts[0])
        self.last_name = name_parts[1].lower()

    def set_given_name(self, first_name):
        if self.first_name == '':
            self.first_name = first_name.lower()

    def set_sex(self, sex):
        self.sex = sex

    def set_private(self):
        self.private = True

    def is_private(self):
        return self.private

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

    def add_object(self, object_id):
        self.objects.append(object_id)

    def add_source(self, source_id):
        self.sources.append(source_id)

    def get_full_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def get_date_range(self):
        if self.can_show_dates():
            start = self.birth_date.get_year_as_text()
            end = self.death_date.get_year_as_text()
            return "{} &ndash; {}".format(start, end)
        else:
            return ''

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
        if self.is_private():
            person = Person(self.id)
            self = person

        value = (
            '  {}'
            '  {}'
        ).format(
            self.image_to_html(),
            self._info_to_html()
        )

        person = HTMLElement('a')
        person.add_attribute('class', 'person')
        person.add_attribute('id', self.id)
        person.add_attribute('href', self.id)
        person.add_attribute('target', '_blank')
        person.set_value(value)

        return str(person)

    def _info_to_html(self):
        value = '{}{}{}{}'.format(
            self.first_name_to_html(),
            self.last_name_to_html(),
            self.date_range_to_html(),
            self.sex_to_html()
        )

        element = HTMLElement('div')
        element.add_attribute('class', 'person-info')
        element.set_value(value)
        return str(element)

    def image_to_html(self, path=''):
        if self.objects:
            path += self.objects[0].file
        else:
            path += 'images/face.png'

        element = HTMLElement('img')
        element.add_attribute('class', 'photo')
        element.add_attribute('src', path)
        return str(element)

    def first_name_to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'first-name')
        element.set_value(self.first_name)
        return str(element)

    def last_name_to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'last-name')
        element.set_value(self.last_name)
        return str(element)

    def sex_to_html(self):
        html = ''
        if self.sex == 'M' or self.sex == 'F':
            element = HTMLElement('img')
            element.add_attribute('class', 'sex')
            element.add_attribute('src', 'images/sex-{}.png'.format(self.sex))
            element.add_attribute('alt', self.sex)
            html = str(element)
        return html

    def date_range_to_html(self):
        dates = ''
        if self.can_show_dates():
            separator = HTMLElement('div')
            separator.add_attribute('class', 'separator')
            separator.set_value('&ndash;')

            dates = self.birth_date.to_html()
            dates += str(separator)
            dates += self.death_date.to_html()

        element = HTMLElement('div')
        element.add_attribute('class', 'date-range')
        element.set_value(dates)

        return str(element)

    def birth_place_to_html(self):
        element_birth_place = HTMLElement('div')
        element_birth_place.add_attribute('class', 'place')
        element_birth_place.set_value(self.birth_place)
        return str(element_birth_place)

    def death_place_to_html(self):
        element_death_place = HTMLElement('div')
        element_death_place.add_attribute('class', 'place')
        element_death_place.set_value(self.death_place)
        return str(element_death_place)

    def sources_to_html(self):
        sources = ''
        for source in self.sources:
            sources += source.to_html()
        for union in self.unions:
            sources += union.sources_to_html()
        return sources

    # pylint: disable=no-self-use
    def _split_name(self, name):
        match = re.search(r'^(.*?)/(.*?)/?\s*$', name)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        else:
            match = re.search(r'^(.*?)/?\s*$', name)
            return ('', match.group(1).strip())

    def __str__(self):
        return "[{} {}]".format(self.first_name, self.last_name)

    def __contains__(self, item):
        return item == self
