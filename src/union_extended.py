from src.node import Node
from src.person import Person
from src.unique_queue import UniqueQueue

class UnionExtended(Node):
    def __init__(self, unions):
        super().__init__()

        self.unions = list()
        self.nodes = list()
        self._extend_nodes(unions)
        self._arrange_unions()

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
        for node in self.nodes:
            html += node.to_html()
        return html

    def _extend_nodes(self, nodes):
        for node in nodes:
            self._extend_node(node)

    def _extend_node(self, node):
        unions = self._extract_all_unions(node)
        for queue_node in unions:
            if queue_node not in self.unions:
                self.unions.append(queue_node)

    # pylint: disable=no-self-use
    def _extract_all_unions(self, node):
        queue = UniqueQueue([node])
        while not queue.is_empty():
            node = queue.pop()
            queue.push_list(node.get_unions())

        return queue.get_all()

    def _arrange_unions(self):
        spouse = self._find_spouse_with_one_union()
        self._add_spouse(spouse)

    def _find_spouse_with_one_union(self):
        for union in self.unions:
            for spouse in union.get_spouses():
                if len(spouse.get_unions()) == 1:
                    return spouse
        print("Warning: group does not have a person with just one union.")
        return Person()

    def _add_spouse(self, spouse):
        if spouse not in self.nodes:
            self.nodes.append(spouse)
            self._add_union_of_spouse(spouse)

    def _add_union_of_spouse(self, spouse):
        union = self._find_next_union(spouse)
        if union is not None:
            self.nodes.append(union.link)
            self._add_spouse(union.get_other_spouse(spouse))

    def _find_next_union(self, spouse):
        for union in spouse.get_unions():
            if union.link not in self.nodes:
                return union

        return None
