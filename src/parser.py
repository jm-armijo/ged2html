import re

from src.date import Date
from src.date_range import DateRange
from src.person import Person
from src.text_line import TextLine
from src.note import Note
from src.object import Object
from src.source import Source
from src.tree import Tree
from src.union import Union

from src.parse_path import ParsePath
from src.element import Element
from src.element_name import Name
from src.element_event import Event
from src.element_file import File

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
        self.unions = list()
        self.objects = dict()
        self.sources = dict()
        self.notes = dict()
        self.tree = None

        self.state = 'IDLE'
        self.current_line = None
        self.path = ParsePath()

    def parse(self, file_name):
        text_lines = self._read_file(file_name)
        self._parse_lines(text_lines)

    def make_tree(self):
        return Tree(self.people, self.unions)

    def get_media_files(self):
        files = list()
        for object in self.objects.values():
            if object.file:
                path = object.file.path
                if path != '':
                    files.append(path)
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
            self.state = self._get_current_state()
            self._parse_current_line()

    def _get_current_state(self):
        new_state = 'IDLE'
        if self.current_line.level == 0 and self.current_line.tag in ['INDI', 'FAM', 'OBJE', 'SOUR', 'NOTE']:
            new_state = self.current_line.tag
        elif self.state == 'INDI' or self.state == 'INDI_DATA':
            if self.current_line.level > 0:
                new_state = 'INDI_DATA'
        elif self.state == 'FAM' or self.state == 'FAM_DATA':
            if self.current_line.level > 0:
                new_state = 'FAM_DATA'
        elif self.state == 'OBJE' or self.state == 'OBJE_DATA':
            if self.current_line.level > 0:
                new_state = 'OBJE_DATA'
        elif self.state == 'SOUR' or self.state == 'SOUR_DATA':
            if self.current_line.level > 0:
                new_state = 'SOUR_DATA'
        elif self.state == 'NOTE' or self.state == 'NOTE_DATA':
            if self.current_line.level > 0:
                new_state = 'NOTE_DATA'

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
        elif self.state == 'SOUR':
            self._create_source()
        elif self.state == 'SOUR_DATA':
            self._add_source_data()
        elif self.state == 'NOTE':
            self._create_note()
        elif self.state == 'NOTE_DATA':
            self._add_note_data()

    def _create_person(self):
        person = self._get_person_or_create(self.current_line.id)
        self.people[person.id] = person
        self.path.set_current(0, 'INDI', person)

    def _create_union(self):
        union = Union(self.current_line.id)
        self.unions.append(union)
        self.path.set_current(0, 'FAM', union)

    def _create_object(self):
        object = self._get_object_or_create(self.current_line.id)
        self.objects[object.id] = object
        self.path.set_current(0, 'OBJE', object)

    def _create_source(self):
        source = self._get_source_or_create(self.current_line.id)
        self.sources[source.id] = source
        self.path.set_current(0, 'SOUR', source)

    def _create_note(self):
        note = self._get_note_or_create(self.current_line.id, self.current_line.data)
        self.notes[note.id] = note
        self.path.set_current(0, 'NOTE', note)

    def _add_person_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data
        child = value

        parent = self.path.get_object_at(level-1)
        parent_key = self.path.get_key_at(level-1)
        if parent == None:
            return

        if tag == 'NAME':
            child = Name(value)
            parent.name = child
        elif tag == 'GIVN':
            child = value
            parent.set_given_name(child)
        elif tag == 'SURN':
            child = value
            parent.set_last_name(value)
        elif tag == 'SEX':
            child = value
            parent.set_gender(child)
        elif tag == 'NATI':
            child = Event(value)
            parent.nationality = child
        elif tag == 'BIRT':
            child = Event()
            parent.birth = child
        elif tag == 'BAPM':
            child = Event()
            parent.baptism = child
        elif tag == 'OCCU':
            child = Event(value)
            parent.occupation = child
        elif tag == 'DEAT':
            child = Event()
            parent.death = child
        elif tag == 'TYPE':
            child = value
            parent.type = child
        elif tag == 'BURI':
            child = Event()
            parent.burial = child
        elif tag == 'OBJE':
            child = self._get_object_or_create(value)
            parent.add_object(child)
        elif tag == '_PRIV':
            child = True
            parent.private = child
        else:
            child = self._add_common_data()

        self.path.set_current(level, tag, child)

    def _add_union_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data

        parent = self.path.get_object_at(level-1)
        if parent == None:
            return

        if tag == 'HUSB':
            child = self._get_person_or_create(value)
            parent.set_spouse1(child)
        elif tag == 'WIFE':
            child = self._get_person_or_create(value)
            parent.set_spouse2(child)
        elif tag == 'CHIL':
            child = self._get_person_or_create(value)
            parent.add_child(child)
        elif tag == 'MARR':
            child = Event()
            parent.marriage = child
        else:
            child = self._add_common_data()

        self.path.set_current(level, tag, child)

    def _add_object_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data

        parent = self.path.get_object_at(level-1)

        if tag == 'FILE':
            child = File(value)
            parent.file = child
        elif tag == 'FORM':
            child = value
            parent.format = child
        elif tag == 'TITL':
            child = value
            parent.title = child
        else:
            child = self._add_common_data()

        self.path.set_current(level, tag, child)

    def _add_source_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data

        parent = self.path.get_object_at(level-1)

        if tag == 'OBJE':
            child = self._get_object_or_create(value)
            parent.add_object(child)
        elif tag == 'TITL':
            child = value
            parent.title = child
        elif tag == 'TEXT':
            child = value
            parent.text = child
        else:
            child = self._add_common_data()

        self.path.set_current(level, tag, child)

    def _add_note_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data

        parent = self.path.get_object_at(level-1)

        if tag == 'CONT':
            child = value
            parent.add_value(child)
        elif tag == 'CONC':
            child = value
            parent.concatenate_value(child)
        else:
            child = self._add_common_data()

        self.path.set_current(level, tag, child)

    def _add_common_data(self):
        level = self.current_line.level
        tag = self.current_line.tag
        value = self.current_line.data

        parent = self.path.get_object_at(level-1)
        parent_key = self.path.get_key_at(level-1)

        if tag == 'SOUR':
            child = self._get_source_or_create(value)
            parent.add_source(child)
        elif tag == 'NOTE':
            child = self._get_note_or_create(value)
            parent.add_note(child)
        elif tag == 'DATE':
            child = self._create_date(value)
            if parent_key != 'CHAN':
                parent.date = child
        elif tag == '_TIME':
            child = value
            parent.date.time = child
        elif tag == 'PLAC':
            child = value
            parent.place = child
        elif tag in ['CHAN', 'TIME', 'FAMC','FAMS']:
            child = Event()
        elif tag in ['_SOSADABOVILLE', '_SOSA']:
            child = value
            parent.sosa = child
        else:
            child = Element()
            print("Unknown child tag '{}' for parent tag '{}'".format(tag, parent_key))

        return child

    def _get_person_or_create(self, person_id):
        person_id = person_id.replace('@', '')
        if person_id not in self.people:
            self.people[person_id] = Person(person_id)

        return self.people[person_id]

    def _get_object_or_create(self, object_id):
        if object_id not in self.objects:
            self.objects[object_id] = Object(object_id)

        return self.objects[object_id]

    def _get_source_or_create(self, source_id):
        if source_id not in self.sources:
            self.sources[source_id] = Source(source_id)

        return self.sources[source_id]

    def _get_note_or_create(self, id, value=''):
        if id not in self.notes:
            self.notes[id] = Note(id)
        self.notes[id].add_value(value)

        return self.notes[id]

    def _create_date(self, raw_date):
        pattern_range = re.compile(r"BET\s(.*)\sAND\s(.*)")
        if pattern_range.match(raw_date):
            match = pattern_range.search(raw_date)
            date = self._parse_range(match.group(1), match.group(2))
        else:
            date = self._parse_date(raw_date)

        return date

    def _parse_date(self, raw_date):
        date = Date()

        pattern = re.compile(r"(ABT|CAL|AFT|BEF|EST)?\s?(\d{1,2})?\s?(\w{3})?\s?(\d{4})")
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

    def _parse_range(self, raw_date1, raw_date2):
        date = DateRange()
        date.start = self._parse_date(raw_date1)
        date.end = self._parse_date(raw_date2)

        return date
