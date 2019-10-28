from src.node import Node
from src.person import Person
from src.html_element import HTMLElement
from src.union_link import UnionLink

class Union(Node):
    def __init__(self, union_id):
        super().__init__()

        self.id = union_id
        self.spouse1 = Person()
        self.spouse2 = Person()
        self.link = UnionLink(union_id)
        self.sources = list()

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

    def set_date(self, date):
        self.link.date = date

    def set_place(self, place):
        self.link.place = place

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

    def is_private(self):
        return self.spouse1.is_private() and self.spouse2.is_private()

    def to_html(self):
        if self.is_private():
            return ''

        value = (
            '  {}\n'
            '  {}\n'
            '  {}\n'
        ).format(
            self.spouse1.to_html(),
            self.link.to_html(),
            self.spouse2.to_html()
        )

        union = HTMLElement('div')
        union.add_attribute('class', 'union')
        union.set_value(value)

        return str(union)

    def sources_to_html(self):
        sources = ''
        for source in self.sources:
            sources += source.to_html()
        return sources

    def __str__(self):
        return str(self.spouse1) + ' oo ' + str(self.spouse2)

    def __contains__(self, item):
        if item in self.spouse1:
            return True
        elif item in self.spouse2:
            return True
        else:
            return False
