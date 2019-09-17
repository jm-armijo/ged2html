from src.edge import Edge
from src.html import HTMLGenerator
from src.tree_level import TreeLevel
from src.tree_node import TreeNode

# pylint: disable=too-few-public-methods
class Tree():

# public:

    def __init__(self, people, unions):
        self.levels = dict()
        self.opened = list()

        self.nodes = self._create_nodes(people)
        self.edges = self._create_edges(unions)

    def to_html(self):
        nodes_html = HTMLGenerator.list_to_html(self.nodes)
        edges_html = HTMLGenerator.list_to_html(self.edges)
        edges_script = HTMLGenerator.get_on_load_script(edges_html)

        return (
            '{}'
            '{}'
        ).format(nodes_html, edges_script)

# private:

    def _create_nodes(self, people):
        level = 0
        starting_node = self._get_starting_node(people)
        if starting_node is not None:
            self._add_node_to_level(starting_node, level)
        return self._levels_to_nodes()

    def _add_nodes_to_level(self, nodes, level):
        for node in nodes:
            self._add_node_to_level(node, level)

    def _add_node_to_level(self, node, level):
        tree_node = TreeNode(node)
        if self._is_opened(tree_node):
            return

        self._open_node(tree_node)
        self._add_to_tree(level, tree_node)

        self._add_nodes_to_level(tree_node.get_children(), level+1)
        self._add_nodes_to_level(tree_node.get_parents(), level-1)

    def _is_opened(self, tree_node):
        nodes = tree_node.get_unions() + tree_node.get_spouses()

        for node in nodes:
            if node in self.opened:
                return True

        return False

    def _open_node(self, tree_node):
        nodes = tree_node.get_unions() + tree_node.get_spouses()

        for node in nodes:
            self.opened.append(node)

    def _create_edges(self, unions):
        edges = list()
        for union in unions:
            edges += self._create_edges_from_node(union)
        return edges

    def _create_edges_from_node(self, start):
        edges = list()
        if start not in self.opened:
            self._notify_element_not_found(start.id)
        else:
            edges = self._create_edges_to_nodes(start, start.get_children())
        return edges

    def _create_edges_to_nodes(self, start, end_nodes):
        edges = list()
        for end in end_nodes:
            edges += self._create_edge_to_node(start, end)
        return edges

    def _create_edge_to_node(self, start, end):
        edges = list()
        if end not in self.opened:
            self._notify_element_not_found(end.id)
        else:
            edges.append(Edge(start.id, end.id))
        return edges

    # pylint: disable=no-self-use
    def _notify_element_not_found(self, element):
        message = (
            "Element {} not processed. "
            "Check your ged file for inconsistent data."
        ).format(element)
        print(message)

    # pylint: disable=no-self-use
    def _get_starting_node(self, people):
        node = None
        people_ids = list(people.keys())

        if people_ids:
            people_ids.sort()
            person_id = people_ids[0]
            node = people[person_id]

        return node

    def _add_to_tree(self, level, node):
        if level not in self.levels:
            self.levels[level] = TreeLevel()
        self.levels[level].append(node)

    def _levels_to_nodes(self):
        keys = sorted(self.levels.keys(), reverse=True)
        nodes = []
        for key in keys:
            nodes.append(self.levels[key])
        return nodes
