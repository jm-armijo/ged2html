from src.node import Node
from src.null_person import NullPerson
from src.html import HTMLGenerator

class Union(Node):
    def __init__(self, id):
        self.id = id
        self.spouse1 = NullPerson()
        self.spouse2 = NullPerson()
        self.children = list()
        self.date = ''
        self.place = ''

    def set_spouse1(self, spouse):
        spouse.add_union(self)
        self.spouse1 = spouse

    def set_spouse2(self, spouse):
        spouse.add_union(self)
        self.spouse2 = spouse

    def add_child(self, child):
        child.set_parents(self)
        self.children.append(child)

    def set_date(self, date):
        self.date = date

    def set_place(self, place):
        self.place = place

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

    def to_html(self):
        value = (
            '  {}\n'
            '  <div class="date" id="{}">{}</div>\n'
            '  {}\n'
        ).format(
            self.spouse1.to_html(),
            self.id,
            self.date,
            self.spouse2.to_html()
        )

        return HTMLGenerator.wrap(self, value)

    def __str__(self):
        to_str = "{{ {} & {} }}".format(self.spouse1, self.spouse2)
        return to_str
