from src.html import HTMLGenerator
from src.person import Person
from src.union_extended import UnionExtended

# pylint: disable=too-few-public-methods
class TreeNode():
    def __init__(self, node):
        self.unions = list()
        self.people = list()

        if isinstance(node, Person) and node.is_single():
            self.node = node
        else:
            self.node = UnionExtended(node.get_unions())

    def get_unions(self):
        return self.node.get_unions()

    def get_spouses(self):
        return self.node.get_spouses()

    def get_children(self):
        return self.node.get_children()

    def get_parents(self):
        return self.node.get_parents()

    def to_html(self):
        value = self.node.to_html()
        return HTMLGenerator.wrap(self, value)
