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

	@patch("src.tree.Tree._ceate_nodes")
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
	# Tree._ceate_nodes
	##########################################

	def test_create_nodes_001(self):
		person = Mock()
		people = Mock()
		nodes = Mock()

		tree = Tree.__new__(Tree)
		tree._get_starting_node = MagicMock(return_value = person)
		tree._extend_node_and_add = MagicMock()
		tree._levels_to_nodes = MagicMock(return_value = nodes)

		return_value = tree._ceate_nodes(people)
		tree._get_starting_node.assert_called_once_with(people)
		tree._extend_node_and_add.assert_called_once_with(0, person)
		tree._levels_to_nodes.assert_called_once_with()
		self.assertEqual(return_value, nodes)

	##########################################
	# Tree._extend_nodes_and_add
	##########################################

	def test_extend_nodes_and_add_001(self):
		level = 4
		node1 = Mock()
		node2 = Mock()
		node3 = Mock()
		nodes = [node1, node2, node3]

		tree = Tree.__new__(Tree)
		tree._extend_node_and_add = MagicMock()

		tree._extend_nodes_and_add(level, nodes)
		self.assertEqual(tree._extend_node_and_add.mock_calls, [call(level, node1), call(level, node2), call(level, node3)])

	def test_extend_nodes_and_add_002(self):
		level = 4
		nodes = list()

		tree = Tree.__new__(Tree)
		tree._extend_node_and_add = MagicMock()

		tree._extend_nodes_and_add(level, nodes)
		tree._extend_node_and_add.assert_not_called()

	##########################################
	# Tree._extend_node_and_add
	##########################################

	def test_extend_node_and_add_001(self):
		level = -3
		node = Mock()
		extended = Mock()

		tree = Tree.__new__(Tree)
		tree._extend_node = MagicMock(return_value = extended)
		tree._add_nodes = MagicMock()

		tree._extend_node_and_add(level, node)
		tree._extend_node.assert_called_once_with(node)
		tree._add_nodes.assert_called_once_with(level, extended)

	##########################################
	# Tree._add_nodes
	##########################################

	def test_add_nodes_001(self):
		level = -3
		nodes = list()
		tree = Tree.__new__(Tree)
		tree._add_node = MagicMock()

		tree._add_nodes(level, nodes)
		tree._add_node.assert_not_called()

	def test_add_nodes_002(self):
		level = -3
		node1 = Mock()
		nodes = [node1]
		tree = Tree.__new__(Tree)
		tree._add_node = MagicMock()

		tree._add_nodes(level, nodes)
		tree._add_node.assert_called_once_with(level, node1)

	def test_add_nodes_003(self):
		level = -3
		node1 = Mock()
		node2 = Mock()
		nodes = [node1, node2]
		tree = Tree.__new__(Tree)
		tree._add_node = MagicMock()

		tree._add_nodes(level, nodes)
		self.assertEqual(tree._add_node.mock_calls, [call(level, node1), call(level, node2)])

	##########################################
	# Tree._add_node
	##########################################

	def test_add_node_001(self):
		level = 5
		children = Mock()
		parents = Mock()
		node = Mock()
		node.id = '@I001@'
		node.get_children = MagicMock(return_value = children)
		node.get_parents = MagicMock(return_value = parents)

		tree = Tree.__new__(Tree)
		tree.opened = list()
		tree._open_node = MagicMock()
		tree._add_to_tree = MagicMock()
		tree._extend_nodes_and_add = MagicMock()

		tree._add_node(level, node)
		tree._open_node.assert_called_once_with(node)
		tree._add_to_tree.assert_called_once_with(level, node)
		self.assertEqual(tree._extend_nodes_and_add.mock_calls, [call(level+1, children), call(level-1, parents)])

	def test_add_node_002(self):
		level = 5
		node = Mock()
		node.id = '@I001@'
		node.get_children = MagicMock()
		node.get_parents = MagicMock()

		tree = Tree.__new__(Tree)
		tree.opened = [node]
		tree._open_node = MagicMock()
		tree._add_to_tree = MagicMock()
		tree._extend_nodes_and_add = MagicMock()

		tree._add_node(level, node)
		tree._open_node.assert_not_called()
		tree._add_to_tree.assert_not_called()
		tree._extend_nodes_and_add.assert_not_called()
		node.get_children.assert_not_called()
		node.get_parents.assert_not_called()

	##########################################
	# Tree._open_node
	##########################################

	def test_open_node_001(self):
		node = Mock()
		tree = Tree.__new__(Tree)
		tree.opened = list()

		tree._open_node(node)
		self.assertEqual(tree.opened, [node])

	def test_open_node_002(self):
		node1 = Mock()
		node2 = Mock()
		tree = Tree.__new__(Tree)
		tree.opened = [node1]

		tree._open_node(node2)
		self.assertEqual(tree.opened, [node1, node2])

	##########################################
	# Tree._extend_nodes
	##########################################

	def test_extend_nodes_001(self):
		nodes = list()
		tree = Tree.__new__(Tree)

		extended = tree._extend_nodes(nodes)
		self.assertEqual(extended, list())

	def test_extend_nodes_002(self):
		nodes = [Mock()]
		extended = [Mock(), Mock()]

		tree = Tree.__new__(Tree)
		tree._extend_node = MagicMock(return_value = extended)

		returned_extended = tree._extend_nodes(nodes)
		self.assertEqual(returned_extended, extended)

	def test_extend_nodes_003(self):
		nodes = [Mock(), Mock()]
		extended1 = [Mock(), Mock()]
		extended2 = [Mock(), Mock(), Mock()]

		tree = Tree.__new__(Tree)
		tree._extend_node = MagicMock(side_effect = [extended1, extended2])

		returned_extended = tree._extend_nodes(nodes)
		self.assertEqual(returned_extended, extended1 + extended2)

	##########################################
	# Tree._extend_node
	##########################################
	def test_extend_node_001(self):
		extended = [Mock(), Mock()]
		node = Mock(spec = Union)

		tree = Tree.__new__(Tree)
		tree._extend_person = MagicMock()
		tree._extend_union = MagicMock(return_value = extended)

		returned_value = tree._extend_node(node)
		tree._extend_person.assert_not_called()
		tree._extend_union.assert_called_once_with(node)
		self.assertEqual(returned_value, extended)

	def test_extend_node_002(self):
		extended = [Mock(), Mock()]
		node = Mock(spec = Person)

		tree = Tree.__new__(Tree)
		tree._extend_person = MagicMock(return_value = extended)
		tree._extend_union = MagicMock()

		returned_value = tree._extend_node(node)
		tree._extend_person.assert_called_once_with(node)
		tree._extend_union.assert_not_called()
		self.assertEqual(returned_value, extended)

	##########################################
	# Tree._extend_person
	##########################################
	def test_extend_peson_001(self):
		person = Mock()
		person.is_single = MagicMock(return_value = True)
		person.get_unions = MagicMock()

		tree = Tree.__new__(Tree)
		tree._open_node = MagicMock()
		tree._extend_nodes = MagicMock()

		extended = tree._extend_person(person)
		person.is_single.assert_called_once_with()
		person.get_unions.assert_not_called()
		tree._open_node.assert_not_called()
		tree._extend_nodes.assert_not_called()
		self.assertEqual(extended, [person])

	def test_extend_peson_002(self):
		unions = Mock()
		person = Mock()
		person.is_single = MagicMock(return_value = False)
		person.get_unions = MagicMock(return_value = unions)

		extended = Mock()
		tree = Tree.__new__(Tree)
		tree._open_node = MagicMock()
		tree._extend_nodes = MagicMock(return_value = extended)

		returned_extended = tree._extend_person(person)
		person.is_single.assert_called_once_with()
		person.get_unions.assert_called_once_with()
		tree._open_node.assert_called_once_with(person)
		tree._extend_nodes.assert_called_once_with(unions)
		self.assertEqual(returned_extended, extended)

	##########################################
	# Tree._extend_union
	##########################################

	'''
	Test when there is nothing to dequeu
	'''
	@patch("src.unique_queue.unique_queue.__new__")
	def test_extend_union_001(self, class_queue):
		all = []

		union = Mock()
		union.get_unions = MagicMock()

		queue = Mock()
		queue.is_empty = MagicMock(return_value = True)
		queue.pop = MagicMock()
		queue.push_list = MagicMock()
		queue.get_all = MagicMock(return_value = all)

		class_queue.return_value = queue

		tree = Tree.__new__(Tree)

		# Checks
		returned_value = tree._extend_union(union)
		queue.is_empty.assert_called_once_with()
		queue.pop.assert_not_called()
		union.get_unions.assert_not_called()
		queue.push_list.assert_not_called()
		queue.get_all.assert_called_once_with()
		self.assertEqual(returned_value, all)

	'''
	Test when the queue has elements
	'''
	@patch("src.unique_queue.unique_queue.__new__")
	def test_extend_union_002(self, class_queue):
		unions = []

		union = Mock()
		union.get_unions = MagicMock(return_value = unions)
		all = Mock()

		queue = Mock()
		queue.is_empty = MagicMock(side_effect = [False, True])
		queue.pop = MagicMock(return_value = union)
		queue.push_list = MagicMock()
		queue.get_all = MagicMock(return_value = all)

		class_queue.return_value = queue

		tree = Tree.__new__(Tree)

		# Checks
		returned_value = tree._extend_union(union)
		self.assertEqual(queue.is_empty.mock_calls, [call(), call()])
		queue.pop.assert_called_once_with()
		union.get_unions.assert_called_once_with()
		queue.push_list.assert_called_once_with(unions)
		queue.get_all.assert_called_once_with()
		self.assertEqual(returned_value, all)

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

	@patch("src.tree.print", create=True)
	def test_create_edges_from_node_001(self, mock_print):
		node = Mock()
		node.id = '@F0002@'

		tree = Tree.__new__(Tree)
		tree._create_edges_to_nodes = MagicMock()
		tree.opened = list()

		return_value = tree._create_edges_from_node(node)
		mock_print.assert_called_with('Element @F0002@ not processed. Check your ged file for inconsistent data.')
		tree._create_edges_to_nodes.assert_not_called()
		self.assertEqual(return_value, list())

	@patch("src.tree.print", create=True)
	def test_create_edges_from_node_002(self, mock_print):
		children = Mock()
		node = Mock()
		node.id = '@F0002@'
		node.get_children = MagicMock(return_value = children)

		edges = Mock()
		tree = Tree.__new__(Tree)
		tree._create_edges_to_nodes = MagicMock(return_value = edges)
		tree.opened = [node]

		return_value = tree._create_edges_from_node(node)
		mock_print.assert_not_called()
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
