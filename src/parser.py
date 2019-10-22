import re

from src.date import Date
from src.person import Person
from src.text_line import TextLine
from src.object import Object
from src.tree import Tree
from src.union import Union

# pylint: disable=too-few-public-methods
class Parser():

    r"""
    The parser implements the state machine below

    ############################################
    #                                          #
    #                    *         +-----+     #
    #                    |         |     |     #
    #                    V         |     V     #
    #             +--->(INDI) -> (INDI_DATA)   #
    #             |                            #
    #             |      *        +------+     #
    #             |      V        |      V     #
    #   * ---> (IDLE)->(OBJE) -> (OBJE_DATA)   #
    #             |                            #
    #             +--->(FAM)  -> (FAM_DATA)    #
    #                    /\        |     /\    #
    #                    |         |     |     #
    #                    *         +-----+     #
    #                                          #
    ############################################
    """

    def __init__(self):
        self.people = dict()
        self.objects = dict()
        self.unions = list()
        self.tree = None

        self.state = 'IDLE'
        self.current_line = None
        self.last_person = None
        self.last_object = None
        self.last_key_per_level = dict()

    def parse(self, file_name):
        text_lines = self._read_file(file_name)
        self._parse_lines(text_lines)

    def make_tree(self):
        return Tree(self.people, self.unions)

    def get_media_files(self):
        files = list()
        for object in self.objects.values():
            if object.file:
                files.append(object.file)
        return files

    # Reads the file into a list of lines
    # pylint: disable=no-self-use
    def _read_file(self, file_name):
        lines = list()
        try:
            with open(file_name, mode='r') as tree_file:
                lines = map(TextLine, tree_file.readlines())
        except FileNotFoundError as error:
            print("Cannot open file '{}': file not found. {}".format(file_name, error))
        except PermissionError as error:
            print("Cannot open file '{}': not enough permissions. {}".format(file_name, error))

        return lines

    def _parse_lines(self, lines):
        for self.current_line in lines:
            self.last_key_per_level[self.current_line.level] = self.current_line.attribute
            self.state = self._get_current_state()
            self._parse_current_line()

    def _get_current_state(self):
        new_state = 'IDLE'
        if self.current_line.level == 0 and self.current_line.data in ['INDI', 'FAM', 'OBJE']:
            new_state = self.current_line.data
        elif self.state == 'INDI' or self.state == 'INDI_DATA':
            if self.current_line.level > 0:
                new_state = 'INDI_DATA'
        elif self.state == 'FAM' or self.state == 'FAM_DATA':
            if self.current_line.level > 0:
                new_state = 'FAM_DATA'
        elif self.state == 'OBJE' or self.state == 'OBJE_DATA':
            if self.current_line.level > 0:
                new_state = 'OBJE_DATA'

        return new_state

    def _parse_current_line(self):
        if self.state == 'INDI':
            self._create_person()
        elif self.state == 'INDI_DATA':
            self._add_person_data()
        elif self.state == 'FAM':
            self._create_union()
        elif self.state == 'FAM_DATA':
            self._add_union_data()
        elif self.state == 'OBJE':
            self._create_object()
        elif self.state == 'OBJE_DATA':
            self._add_object_data()

    def _create_person(self):
        person = self._get_person_or_create(self.current_line.attribute)
        self.people[person.id] = person
        self.last_person = person.id

    def _add_person_data(self):
        level = self.current_line.level
        attribute = self.current_line.attribute
        value = self.current_line.data

        person = self.people[self.last_person]

        if attribute == 'NAME':
            person.set_name(value)
        elif attribute == 'GIVN':
            person.set_given_name(value)
        elif attribute == 'SEX':
            person.set_sex(value)
        elif attribute == 'OBJE':
            object = self._get_object_or_create(value)
            person.add_object(object)
        elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'BIRT':
            date = self._create_date(value)
            person.set_birth_date(date)
        elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'DEAT':
            date = self._create_date(value)
            person.set_death_date(date)
        elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'BIRT':
            person.set_birth_place(value)
        elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'DEAT':
            person.set_death_place(value)

    def _create_union(self):
        union = Union(self.current_line.attribute)
        self.unions.append(union)

    def _add_union_data(self):
        level = self.current_line.level
        attribute = self.current_line.attribute
        value = self.current_line.data

        union = self.unions[-1]

        if attribute == 'HUSB':
            union.set_spouse1(self._get_person_or_create(value))
        elif attribute == 'WIFE':
            union.set_spouse2(self._get_person_or_create(value))
        elif attribute == 'CHIL':
            union.add_child(self._get_person_or_create(value))
        elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'MARR':
            date = self._create_date(value)
            union.set_date(date)
        elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'MARR':
            union.set_place(value)

    def _create_object(self):
        object = self._get_object_or_create(self.current_line.attribute)
        self.objects[object.id] = object
        self.last_object = object.id

    def _add_object_data(self):
        level = self.current_line.level
        attribute = self.current_line.attribute
        value = self.current_line.data

        object = self.objects[self.last_object]

        if attribute == 'FILE':
            object.set_file(value)
        elif attribute == 'FORM':
            object.set_format(value)

    def _get_person_or_create(self, person_id):
        person_id = person_id.replace('@', '')
        if person_id not in self.people:
            self.people[person_id] = Person(person_id)

        return self.people[person_id]

    def _get_object_or_create(self, object_id):
        if object_id not in self.objects:
            self.objects[object_id] = Object(object_id)

        return self.objects[object_id]

    def _create_date(self, raw_date):
        date = Date()

        pattern = re.compile(r"(ABT|AFT|BEF|EST)?\s?(\d{1,2})?\s?(\w{3})?\s?(\d{4})")
        if pattern.match(raw_date):
            match = pattern.search(raw_date)
            if match.group(1):
                date.precision = match.group(1)
            if match.group(2):
                date.day = match.group(2)
            if match.group(3):
                date.month = match.group(3)
            date.year = match.group(4)
        elif raw_date != '':
            print("Unable to parse date '{}'".format(raw_date))

        return date
