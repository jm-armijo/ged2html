from src.node import Node
from src.person import Person
from src.unique_queue import UniqueQueue

class UnionExtended(Node):
    def __init__(self, unions):
        super().__init__()

        self.unions = list()
        self.nodes = list()
        unions = self._extend_nodes(unions)
        self._arrange_unions(unions)
        self._sort_unions()

    def get_unions(self):
        return self.unions

    def get_birth_year(self):
        years = list()
        for spouse in self.get_spouses():
            years.append(spouse.birth.date.get_year())
        return min(years)

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

    def is_private(self):
        for node in self.nodes:
            if not node.is_private():
                return False

        return True

    def _extend_nodes(self, nodes):
        unions = set()
        for node in nodes:
            unions |= self._extract_all_unions(node)
        return unions

    # pylint: disable=no-self-use
    def _extract_all_unions(self, node):
        queue = UniqueQueue([node])
        while not queue.is_empty():
            node = queue.pop()
            queue.push_list(node.get_unions())

        return set(queue.get_all())

    def _arrange_unions(self, unions):
        spouse = self._find_spouse_with_one_union(unions)
        self._add_spouse(spouse)

    def _sort_unions(self):
        dates = self._get_union_dates()
        if dates and dates[0] > dates[-1]:
            self.nodes.reverse()
            self.unions.reverse()

    def _get_union_dates(self):
        dates = list()
        for union in self.unions:
            year = union.marriage.date.get_year()
            if int(year) < 3000:
                dates.append(year)

        return dates

    def _find_spouse_with_one_union(self, unions):
        for union in unions:
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
            self.unions.append(union)
            self.nodes.append(union)
            self._add_spouse(union.get_other_spouse(spouse))

    def _find_next_union(self, spouse):
        for union in spouse.get_unions():
            if union not in self.nodes:
                return union

        return None

    def __str__(self):
        return ' '.join(map(str, self.nodes))

    def __contains__(self, item):
        for union in self.unions:
            if item in union:
                return True
        return False
