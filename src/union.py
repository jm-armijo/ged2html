from src.node import Node
from src.person import Person
from src.element_event import Event

class Union(Node):
    def __init__(self, union_id):
        super().__init__()

        self.id = union_id
        self.spouse1 = Person()
        self.spouse2 = Person()
        self.marriage = Event()

    def set_spouse1(self, spouse):
        spouse.add_union(self)
        self.spouse1 = spouse

    def set_spouse2(self, spouse):
        spouse.add_union(self)
        self.spouse2 = spouse

    def add_child(self, child):
        child.set_parents(self)
        self.children.append(child)

    def add_source(self, source_id):
        self.sources.append(source_id)

    def get_spouses(self):
        people = list()
        people.append(self.spouse1)
        people.append(self.spouse2)
        return people

    def get_other_spouse(self, spouse):
        if spouse == self.spouse1:
            return self.spouse2
        elif spouse == self.spouse2:
            return self.spouse1
        else:
            return None

    def get_children(self):
        return self.children

    def get_parents(self):
        parents = list()
        if self.spouse1 is not None:
            parents += self.spouse1.get_parents()
        if self.spouse2 is not None:
            parents += self.spouse2.get_parents()

        return parents

    def get_unions(self):
        parents = list()
        if self.spouse1 is not None:
            parents += self.spouse1.get_unions()
        if self.spouse2 is not None:
            parents += self.spouse2.get_unions()

        return parents

    def get_sources(self):
        sources = self.marriage.sources
        return sources

    def is_private(self):
        return self.spouse1.is_private() and self.spouse2.is_private()

    def __str__(self):
        return 'oo ({})'.format(self.id)

    def __contains__(self, item):
        if item in self.spouse1:
            return True
        elif item in self.spouse2:
            return True
        else:
            return False
