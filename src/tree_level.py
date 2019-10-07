from src.ordered_set import OrderedSet
from src.html import HTMLGenerator

class TreeLevel():
    def __init__(self):
        self.nodes = list()

    def append(self, node):
        self.nodes.append(node)

    def sort_nodes_giving_priority(self, children):
        nodes = OrderedSet()

        for child in children:
            nodes.append_list(self._find_node_having_person(child))

        # Appending nodes with no children: already added nodes won't be added again.
        nodes.append_list(self.nodes)

        # Overriding list of nodes
        self.nodes = nodes.to_list()

    def get_children(self):
        children = list()
        for node in self.nodes:
            children += node.get_children()
        return children

    def to_html(self):
        value = HTMLGenerator.list_to_html(self.nodes)
        return HTMLGenerator.wrap_instance(self, value)

    def _find_node_having_person(self, person):
        for node in self.nodes:
            if person in node:
                return [node]
        return list()
