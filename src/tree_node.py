from src.html_element import HTMLElement
from src.person import Person
from src.union_extended import UnionExtended

# pylint: disable=too-few-public-methods
class TreeNode():
    def __init__(self, node):
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
        if self.node.is_private():
            return ''

        value = self.node.to_html()

        node = HTMLElement('div')
        node.add_attribute('class', 'treenode')
        node.set_value(value)

        return str(node)

    def __str__(self):
        return str(self.node)

    def __contains__(self, item):
        return item in self.node
