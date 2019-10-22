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
        self.life_period = DateRange()
        self.birth_place = ''
        self.death_place = ''
        self.unions = list()
        self.objects = list()

    def get_pronoun(self):
        if self.sex == 'M':
            return 'he'
        elif self.sex == 'F':
            return 'she'
        else:
            return 'they'

    def can_show_dates(self):
        start = self.life_period.start
        end = self.life_period.end
        limit = datetime.datetime.now().year - 100

        if not end.is_empty() or (not start.is_empty() and int(start.year) < limit):
            return True
        else:
            return False

    def get_birth_date(self):
        if self.can_show_dates():
            return self.life_period.start
        else:
            return Date()

    def get_death_date(self):
        if self.can_show_dates():
            return self.life_period.end
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

    def set_birth_date(self, date):
        self.life_period.start = date

    def set_birth_place(self, place):
        self.birth_place = place

    def set_death_date(self, date):
        self.life_period.end = date

    def set_death_place(self, place):
        self.death_place = place

    def set_parents(self, parents):
        self.parents.append(parents)

    def add_union(self, union):
        self.unions.append(union)
        self.children += union.get_children()

    def add_object(self, object_id):
        self.objects.append(object_id)

    def get_full_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def get_date_range(self):
        if self.can_show_dates():
            return str(self.life_period)
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
        life_period = ''
        if self.can_show_dates():
            life_period = self.life_period.to_html()

        value = '{}{}{}{}'.format(
            self.first_name_to_html(),
            self.last_name_to_html(),
            life_period,
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
        element_date_range = HTMLElement('div')
        element_date_range.add_attribute('class', 'date-range')
        element_date_range.set_value(self.life_period.to_html())
        return str(element_date_range)

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
