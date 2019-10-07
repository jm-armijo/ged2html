import re
from src.html import HTMLGenerator
from src.node import Node
from src.date_range import DateRange
from src.html_element import HTMLElement

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
            self._image_to_html(),
            self._info_to_html()
        )
        return HTMLGenerator.wrap_instance(self, value, self.id)

    def _info_to_html(self):
        value = '{}{}{}{}'.format(
            self._give_name_to_html(),
            self._last_name_to_html(),
            self.life_period.to_html(),
            self._sex_to_html()
        )

        element = HTMLElement('div')
        element.add_attribute('class', 'person-info')
        element.set_value(value)
        return str(element)

    def _image_to_html(self):
        if self.objects:
            path = self.objects[0].file
        else:
            path = 'images/face.png'

        element = HTMLElement('img')
        element.add_attribute('class', 'photo')
        element.add_attribute('src', path)
        return str(element)

    def _give_name_to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'first-name')
        element.set_value(self.first_name)
        return str(element)

    def _last_name_to_html(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'last-name')
        element.set_value(self.last_name)
        return str(element)


    def _sex_to_html(self):
        html = ''
        if self.sex == 'M' or self.sex == 'F':
            element = HTMLElement('img')
            element.add_attribute('class', 'sex')
            element.add_attribute('src', 'images/sex-{}.png'.format(self.sex))
            element.add_attribute('alt', self.sex)
            html = str(element)
        return html

    # pylint: disable=no-self-use
    def _split_name(self, name):
        match = re.search(r'^(.*?)/(.*?)/?\s*$', name)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        else:
            print("Unable to get first and last name from '{}'".format(name))
            return ('', '')

    def __str__(self):
        return "[{} {}]".format(self.first_name, self.last_name)

    def __contains__(self, item):
        return item == self
