import unittest
from unittest.mock import Mock, patch, MagicMock, call, ANY
from ..html import HTMLGenerator
from ..person import Person
from ..tree import Tree
from ..tree_level import TreeLevel
from ..union import Union

class TestTree(unittest.TestCase):

    ##########################################
    # Tree.init
    ##########################################

    @patch("src.tree.Tree._create_nodes")
    @patch("src.tree.Tree._create_edges")
    def test_init_001(self, mock_edges, mock_nodes):
        nodes = Mock()
        edges = Mock()
        mock_nodes.return_value = nodes
        mock_edges.return_value = edges

        people = Mock()
        unions = Mock()
        tree = Tree(people, unions)

        self.assertEqual(tree.levels, dict())
        self.assertEqual(tree.opened, list())
        self.assertEqual(tree.nodes, nodes)
        self.assertEqual(tree.edges, edges)

        mock_edges.assert_called_once_with(unions)
        mock_nodes.assert_called_once_with(people)

    ##########################################
    # Tree.to_html
    ##########################################

    def test_to_html_001(self):
        # Mock HTMLGenerator methods
        nodes = Mock()
        edges = Mock()

        nodes_html = '<div>X</div>'
        edges_html = '<div>Y</div>'
        on_load = '<script>Z</script>'
        expected = nodes_html + on_load

        HTMLGenerator.list_to_html = MagicMock(side_effect = [nodes_html, edges_html])
        HTMLGenerator.get_on_load_script = MagicMock(return_value = on_load)

        # Mock Tree class
        tree = Tree.__new__(Tree)
        tree.nodes = nodes
        tree.edges = edges

        # Actual test
        actual = tree.to_html()
        list_to_html_calls = HTMLGenerator.list_to_html.mock_calls
        self.assertEqual(list_to_html_calls, [call(nodes), call(edges)])
        HTMLGenerator.get_on_load_script.assert_called_once_with(edges_html)
        self.assertEqual(expected, actual)

    ##########################################
    # Tree._create_nodes
    ##########################################

    def test_create_nodes_001(self):
        person = Mock()
        people = Mock()
        nodes = Mock()

        tree = Tree.__new__(Tree)
        tree._get_starting_node = MagicMock(return_value = person)
        tree._add_node_to_level = MagicMock()
        tree._levels_to_nodes = MagicMock(return_value = nodes)

        return_value = tree._create_nodes(people)
        tree._get_starting_node.assert_called_once_with(people)
        tree._add_node_to_level.assert_called_once_with(person, 0)
        tree._levels_to_nodes.assert_called_once_with()
        self.assertEqual(return_value, nodes)

    ##########################################
    # Tree._add_nodes_to_level
    ##########################################

    def test_add_nodes_001(self):
        level = -3
        nodes = list()
        tree = Tree.__new__(Tree)
        tree._add_node_to_level = MagicMock()

        tree._add_nodes_to_level(nodes, level)
        tree._add_node_to_level.assert_not_called()

    def test_add_nodes_002(self):
        level = -3
        node1 = Mock()
        nodes = [node1]
        tree = Tree.__new__(Tree)
        tree._add_node_to_level = MagicMock()

        tree._add_nodes_to_level(nodes, level)
        tree._add_node_to_level.assert_called_once_with(node1, level)

    def test_add_nodes_003(self):
        level = -3
        node1 = Mock()
        node2 = Mock()
        nodes = [node1, node2]
        tree = Tree.__new__(Tree)
        tree._add_node_to_level = MagicMock()

        tree._add_nodes_to_level(nodes, level)
        self.assertEqual(tree._add_node_to_level.mock_calls, [call(node1, level), call(node2, level)])

    ##########################################
    # Tree._add_node_to_level
    ##########################################

    @patch("src.tree_node.TreeNode.__new__")
    def test_add_node_to_level_001(self, class_tree_node):
        children = Mock()
        parents = Mock()

        tree_node = Mock()
        tree_node.get_children = MagicMock(return_value = children)
        tree_node.get_parents = MagicMock(return_value = parents)
        class_tree_node.return_value = tree_node

        tree = Tree.__new__(Tree)
        tree._is_opened = MagicMock(return_value = False)
        tree._open_node = MagicMock()
        tree._add_to_tree = MagicMock()
        tree._add_nodes_to_level = MagicMock()

        level = 5
        node = Mock()
        tree._add_node_to_level(node, level)

        class_tree_node.assert_called_once_with(ANY, node)
        tree._is_opened.assert_called_once_with(tree_node)
        tree._open_node.assert_called_once_with(tree_node)
        tree._add_to_tree.assert_called_once_with(level, tree_node)
        self.assertEqual(tree._add_nodes_to_level.mock_calls, [call(children, level+1), call(parents, level-1)])

    @patch("src.tree_node.TreeNode.__new__")
    def test_add_node_to_level_002(self, class_tree_node):
        children = Mock()
        parents = Mock()

        tree_node = Mock()
        tree_node.get_children = MagicMock(return_value = children)
        tree_node.get_parents = MagicMock(return_value = parents)
        class_tree_node.return_value = tree_node

        tree = Tree.__new__(Tree)
        tree._is_opened = MagicMock(return_value = True)
        tree._open_node = MagicMock()
        tree._add_to_tree = MagicMock()
        tree._add_nodes_to_level = MagicMock()

        level = 5
        node = Mock()
        tree._add_node_to_level(node, level)

        class_tree_node.assert_called_once_with(ANY, node)
        tree._is_opened.assert_called_once_with(tree_node)
        tree._open_node.assert_not_called()
        tree._add_to_tree.assert_not_called()
        tree._add_nodes_to_level.assert_not_called()

    ##########################################
    # Tree._is_opened
    ##########################################

    def test_is_opened_001(self):
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = list()

        actual = tree._is_opened(tree_node)
        self.assertEqual(actual, False)

    def test_is_opened_002(self):
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = [union]

        actual = tree._is_opened(tree_node)
        self.assertEqual(actual, True)

    def test_is_opened_003(self):
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = [spouse2]

        actual = tree._is_opened(tree_node)
        self.assertEqual(actual, True)

    def test_is_opened_004(self):
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = [union, spouse1, spouse2]

        actual = tree._is_opened(tree_node)
        self.assertEqual(actual, True)

    ##########################################
    # Tree._open_node
    ##########################################

    def test_open_node_001(self):
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = list()

        tree._open_node(tree_node)
        self.assertEqual(tree.opened, [union, spouse1, spouse2])

    def test_open_node_002(self):
        dummy = Mock()
        union = Mock()
        spouse1 = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse1, spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = [dummy]

        tree._open_node(tree_node)
        self.assertEqual(tree.opened, [dummy, union, spouse1, spouse2])

    def test_open_node_003(self):
        union = Mock()
        spouse2 = Mock()

        tree_node = Mock()
        tree_node.get_unions = MagicMock(return_value = [union])
        tree_node.get_spouses = MagicMock(return_value = [spouse2])

        tree = Tree.__new__(Tree)
        tree.opened = list()

        tree._open_node(tree_node)
        self.assertEqual(tree.opened, [union, spouse2])

    ##########################################
    # Tree._create_edges
    ##########################################

    def test_create_edges_001(self):
        unions = list()
        edges = list()

        tree = Tree.__new__(Tree)
        tree._create_edges_from_node = MagicMock()

        return_value = tree._create_edges(unions)
        tree._create_edges_from_node.assert_not_called()
        self.assertEqual(return_value, edges)

    def test_create_edges_002(self):
        union1 = Mock()
        union2 = Mock()
        unions = [union1, union2]

        edges_union1 = [Mock(), Mock()]
        edges_union2 = [Mock()]

        tree = Tree.__new__(Tree)
        tree._create_edges_from_node = MagicMock(side_effect = [edges_union1, edges_union2])

        return_value = tree._create_edges(unions)
        self.assertEqual(tree._create_edges_from_node.mock_calls, [call(union1), call(union2)])
        self.assertEqual(return_value, edges_union1 + edges_union2)

    ##########################################
    # Tree._create_edges_from_node
    ##########################################

    def test_create_edges_from_node_001(self):
        node = Mock()
        node.id = '@F0002@'

        tree = Tree.__new__(Tree)
        tree._create_edges_to_nodes = MagicMock()
        tree._notify_element_not_found = MagicMock()
        tree.opened = list()

        return_value = tree._create_edges_from_node(node)
        tree._notify_element_not_found.assert_called_with(node.id)
        tree._create_edges_to_nodes.assert_not_called()
        self.assertEqual(return_value, list())

    def test_create_edges_from_node_002(self):
        children = Mock()
        node = Mock()
        node.id = '@F0002@'
        node.get_children = MagicMock(return_value = children)

        edges = Mock()
        tree = Tree.__new__(Tree)
        tree._create_edges_to_nodes = MagicMock(return_value = edges)
        tree._notify_element_not_found = MagicMock()
        tree.opened = [node]

        return_value = tree._create_edges_from_node(node)
        tree._notify_element_not_found.assert_not_called()
        tree._create_edges_to_nodes.assert_called_once_with(node, children)
        self.assertEqual(return_value, edges)

    ##########################################
    # Tree._create_edges_to_nodes
    ##########################################

    def test_create_edges_to_nodes_001(self):
        tree = Tree.__new__(Tree)
        tree._create_edge_to_node = MagicMock()

        start = Mock()
        nodes = list()
        edges = list()

        return_value = tree._create_edges_to_nodes(start, nodes)
        tree._create_edge_to_node.assert_not_called()
        self.assertEqual(return_value, edges)

    def test_create_edges_to_nodes_002(self):
        edge1 = Mock()
        edge2 = Mock()
        edges = [edge1, edge2]
        tree = Tree.__new__(Tree)
        tree._create_edge_to_node = MagicMock(side_effect = [[edge1], [edge2]])

        start = Mock()
        node1 = Mock()
        node2 = Mock()
        nodes = [node1, node2]

        return_value = tree._create_edges_to_nodes(start, nodes)
        self.assertEqual(tree._create_edge_to_node.mock_calls, [call(start, node1), call(start, node2)])
        self.assertEqual(return_value, edges)

    ##########################################
    # Tree._create_edge_to_node
    ##########################################

    @patch("src.tree.print", create=True)
    @patch("src.edge.Edge.__new__")
    def test_create_edge_to_node_001(self, mock_edge, mock_print):
        start = Mock()
        node = Mock()
        node.id = '@I0002@'

        tree = Tree.__new__(Tree)
        tree.opened = list()

        return_value = tree._create_edge_to_node(start, node)
        mock_print.assert_called_with('Element @I0002@ not processed. Check your ged file for inconsistent data.')
        mock_edge.assert_not_called()
        self.assertEqual(return_value, list())

    @patch("src.tree.print", create=True)
    @patch("src.edge.Edge.__new__")
    def test_create_edge_to_node_002(self, mock_edge, mock_print):
        edge = Mock()
        mock_edge.return_value = edge

        start = Mock()
        start.id = '@F0001@'
        node = Mock()
        node.id = '@I0002@'

        tree = Tree.__new__(Tree)
        tree.opened = [Mock(), Mock(), node, Mock()]

        return_value = tree._create_edge_to_node(start, node)
        mock_print.assert_not_called()
        mock_edge.assert_called_once_with(ANY, start.id, node.id)
        self.assertEqual(return_value, [edge])

    ##########################################
    # Tree._notify_element_not_found
    ##########################################

    @patch("src.tree.print", create=True)
    def test_notify_element_not_found_001(self, mock_print):
        value = 'X'
        expected = 'Element X not processed. Check your ged file for inconsistent data.'

        tree = Tree.__new__(Tree)
        tree._notify_element_not_found(value)
        mock_print.assert_called_with(expected)

    ##########################################
    # Tree._get_starting_node
    ##########################################

    def test_get_starting_person_001(self):
        # Setup people
        person1 = None
        people = dict()

        # Setup Tree
        tree = Tree.__new__(Tree)

        # Actual test
        returned_person = tree._get_starting_node(people)
        self.assertEqual(returned_person, person1)

    def test_get_starting_person_002(self):
        # Setup people
        id1 = '@I0001234@'
        person1 = Mock()
        people = {id1:person1}

        # Setup Tree
        tree = Tree.__new__(Tree)

        # Actual test
        returned_person = tree._get_starting_node(people)
        self.assertEqual(returned_person, person1)

    def test_get_starting_person_003(self):
        # Setup people
        id1 = '@I0001234@'
        id2 = '@I0001233@'
        person1 = Mock()
        person2 = Mock()
        people = {id1:person1, id2:person2}

        # Setup Tree
        tree = Tree.__new__(Tree)

        # Actual test
        returned_person = tree._get_starting_node(people)
        self.assertEqual(returned_person, person2)

    ##########################################
    # Tree._add_to_tree
    ##########################################

    @patch("src.tree_level.TreeLevel.__new__")
    def test_add_to_tree_001(self, class_tree_level):
        node = Mock()

        level_1 = Mock()
        level_1.append = MagicMock()
        class_tree_level.return_value = level_1

        tree = Tree.__new__(Tree)
        tree.levels = dict()

        tree._add_to_tree(1, node)
        class_tree_level.assert_called_once()
        level_1.append.assert_called_once_with(node)

    @patch("src.tree_level.TreeLevel.__new__")
    def test_add_to_tree_002(self, class_tree_level):
        node = Mock()

        level_1 = Mock()
        level_1.append = MagicMock()

        tree = Tree.__new__(Tree)
        tree.levels = {1: level_1}

        tree._add_to_tree(1, node)
        class_tree_level.assert_not_called()
        level_1.append.assert_called_once_with(node)

    ##########################################
    # Tree._levels_to_nodes
    ##########################################

    def test_levels_to_nodes_001(self):
        node1 = Mock()
        node2 = Mock()
        node3 = Mock()

        tree = Tree.__new__(Tree)
        tree.levels = {1: node1, 2: node2, 3:node3}

        return_value = tree._levels_to_nodes()
        self.assertEqual(return_value, [node3, node2, node1])

    def test_levels_to_nodes_002(self):
        node1 = Mock()
        node2 = Mock()
        node3 = Mock()

        tree = Tree.__new__(Tree)
        tree.levels = {2: node2, 1: node1, 3:node3}

        return_value = tree._levels_to_nodes()
        self.assertEqual(return_value, [node3, node2, node1])

    def test_levels_to_nodes_003(self):
        node1 = Mock()
        node2 = Mock()
        node3 = Mock()

        tree = Tree.__new__(Tree)
        tree.levels = {3: node3, 2: node2, 1: node1}

        return_value = tree._levels_to_nodes()
        self.assertEqual(return_value, [node3, node2, node1])

if __name__ == '__main__':
    unittest.main()
