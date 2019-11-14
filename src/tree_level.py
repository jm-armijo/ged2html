from src.ordered_set import OrderedSet

class TreeLevel():
    def __init__(self):
        self.nodes = list()

    def append(self, node):
        self.nodes.append(node)

    def node_unions_in_list(self, node, list):
        unions = node.get_unions()
        for union in unions:
            if union in list:
                return True
        return False

    def sort_nodes_giving_priority(self, preordered_unions):
        self.nodes.sort(key=lambda node: node.node.get_birth_year())
        presorted_nodes = self.get_nodes_for_preordered_unions(preordered_unions)
        self.nodes = self.add_non_preordered_nodes(presorted_nodes)

    def get_nodes_for_preordered_unions(self, preordered_unions):
        presorted_nodes = list()
        for union in preordered_unions:
            node = self.find_node_having_union(union)
            if node is not None and node not in presorted_nodes:
                presorted_nodes.append(node)

        return presorted_nodes

    def add_non_preordered_nodes(self, presorted_nodes):
        sorted_nodes = list()
        idx = 0
        for node in self.nodes:
            if node in presorted_nodes:
                pre = presorted_nodes[idx]
                idx += 1
                sorted_nodes.append(pre)
            else:
                sorted_nodes.append(node)

        return sorted_nodes

    def find_node_having_union(self, union):
        for node in self.nodes:
            if union in node.get_unions():
                return node

        return None

    def get_children(self):
        children = list()
        for node in self.nodes:
            children += node.get_children()
        return children

    def get_parents(self):
        parents = list()
        for node in self.nodes:
            if not node.node.is_private():
                parents += node.get_parents()
        return parents

    def _find_node_having_person(self, person):
        for node in self.nodes:
            if person in node:
                return [node]
        return list()
