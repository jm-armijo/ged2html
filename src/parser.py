from src.text_line import TextLine
from src.person import Person
from src.tree import Tree
from src.union import Union

class Parser():
    def __init__(self):
        self.people = dict()
        self.unions = list()
        self.tree = None

        self.state = 'IDLE'
        self.current_line = None
        self.last_person = None
        self.last_key_per_level = dict()

    def make_tree(self, file_name):
        text_lines = self._read_file(file_name)
        self._parse_lines(text_lines)

        return Tree(self.people, self.unions)

    # Reads the file into a list of lines
    def _read_file(self, file_name):
        with open(file_name,mode='r') as tree_file:
            return map(TextLine, tree_file.readlines())

    def _parse_lines(self, lines):
        for self.current_line in lines:
            self.last_key_per_level[self.current_line.level] = self.current_line.attribute
            self.state = self._get_current_state()
            self._parse_current_line()

    '''
    _get_current_state: implements the state machine below
    in: current state
    returns: new state

    ############################################
    #                                          #
    #                    *         +-----+     #
    #                    |         |     |     #
    #                    V         |     V     #
    #             +--->(INDI) -> (INDI_DATA)   #
    #             |                            #
    #   * ---> (IDLE)                          #
    #             |                            #
    #             +--->(FAM)  -> (FAM_DATA)    #
    #                    /\        |     /\    #
    #                    |         |     |     #
    #                    *         +-----+     #
    #                                          #
    ############################################
    '''

    def _get_current_state(self):
        new_state = 'IDLE'
        if self.current_line.level == 0 and self.current_line.data in ['INDI', 'FAM']:
            new_state = self.current_line.data
        elif self.state == 'INDI' or self.state == 'INDI_DATA':
            if self.current_line.level > 0:
                new_state = 'INDI_DATA'
        elif self.state == 'FAM' or self.state == 'FAM_DATA':
            if self.current_line.level > 0:
                new_state = 'FAM_DATA'

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

    def _create_person(self):
        person = self._get_person_or_create(self.current_line.attribute)
        self.people[person.id] = person
        self.last_person = person.id

    def _add_person_data(self):
        level = self.current_line.level
        attribute = self.current_line.attribute
        value  = self.current_line.data

        person = self.people[self.last_person]

        if attribute == 'NAME':
            person.set_name(value)
        elif attribute == 'GIVN':
            person.set_given_name(value)
        elif attribute == 'SEX':
            person.set_sex(value)
        elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'BIRT':
            person.set_birth_date(value)
        elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'BIRT':
            person.set_birth_place(value)

    def _create_union(self):
        union = Union(self.current_line.attribute)
        self.unions.append(union)

    def _add_union_data(self):
        level = self.current_line.level
        attribute = self.current_line.attribute
        value  = self.current_line.data

        union = self.unions[-1]

        if attribute == 'HUSB':
            union.set_spouse1(self._get_person_or_create(value))
        elif attribute == 'WIFE':
            union.set_spouse2(self._get_person_or_create(value))
        elif attribute == 'CHIL':
            union.add_child(self._get_person_or_create(value))
        elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'MARR':
            union.set_date(value)
        elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'MARR':
            union.set_place(value)

    def _get_person_or_create(self, id):
        if id not in self.people:
            self.people[id] = Person(id)

        return self.people[id]

