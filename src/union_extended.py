from src.node import Node
from src.unique_queue import UniqueQueue

class UnionExtended(Node):
    def __init__(self, unions):
        super().__init__()

        self.unions = list()
        self._extend_nodes(unions)

    def get_unions(self):
        return self.unions

    def get_spouses(self):
        people = list()
        for union in self.unions:
            people += union.get_spouses()
        return people

    def get_parents(self):
        parents = []
        for union in self.unions:
            parents += union.get_parents()
        return parents

    def get_children(self):
        children = []
        for union in self.unions:
            children += union.get_children()
        return children

    def to_html(self):
        html = ''
        for union in self.unions:
            html += union.to_html()
        return html

    def _extend_nodes(self, nodes):
        for node in nodes:
            self._extend_node(node)

    # pylint: disable=no-self-use
    def _extend_node(self, node):
        unions = self._extract_all_unions(node)
        for queue_node in unions:
            if queue_node not in self.unions:
                self.unions.append(queue_node)

    def _extract_all_unions(self, node):
        queue = UniqueQueue([node])
        while not queue.is_empty():
            node = queue.pop()
            queue.push_list(node.get_unions())

        return queue.get_all()
