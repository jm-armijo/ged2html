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

	@patch("src.tree.Tree._createNodes")
	@patch("src.tree.Tree._createEdges")
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
	# Tree.toHTML
	##########################################

	def test_to_html_001(self):
		# Mock HTMLGenerator methods
		nodes = Mock()
		edges = Mock()

		nodes_html = '<div>X</div>'
		edges_html = '<div>Y</div>'
		on_load = '<script>Z</script>'
		expected = nodes_html + on_load

		HTMLGenerator.listToHTML = MagicMock(side_effect = [nodes_html, edges_html])
		HTMLGenerator.getOnLoadScript = MagicMock(return_value = on_load)

		# Mock Tree class
		tree = Tree.__new__(Tree)
		tree.nodes = nodes
		tree.edges = edges

		# Actual test
		actual = tree.toHTML()
		list_to_html_calls = HTMLGenerator.listToHTML.mock_calls
		self.assertEqual(list_to_html_calls, [call(nodes), call(edges)])
		HTMLGenerator.getOnLoadScript.assert_called_once_with(edges_html)
		self.assertEqual(expected, actual)

	##########################################
	# Tree._createNodes
	##########################################

	def test_create_nodes_001(self):
		person = Mock()
		people = Mock()
		nodes = Mock()

		tree = Tree.__new__(Tree)
		tree._getStartingNode = MagicMock(return_value = person)
		tree._extendNodeAndAdd = MagicMock()
		tree._levelsToNodes = MagicMock(return_value = nodes)

		return_value = tree._createNodes(people)
		tree._getStartingNode.assert_called_once_with(people)
		tree._extendNodeAndAdd.assert_called_once_with(0, person)
		tree._levelsToNodes.assert_called_once_with()
		self.assertEqual(return_value, nodes)

	##########################################
	# Tree._extendNodesAndAdd
	##########################################

	def test_extend_nodes_and_add_001(self):
		level = 4
		node1 = Mock()
		node2 = Mock()
		node3 = Mock()
		nodes = [node1, node2, node3]

		tree = Tree.__new__(Tree)
		tree._extendNodeAndAdd = MagicMock()

		tree._extendNodesAndAdd(level, nodes)
		self.assertEqual(tree._extendNodeAndAdd.mock_calls, [call(level, node1), call(level, node2), call(level, node3)])

	def test_extend_nodes_and_add_002(self):
		level = 4
		nodes = list()

		tree = Tree.__new__(Tree)
		tree._extendNodeAndAdd = MagicMock()

		tree._extendNodesAndAdd(level, nodes)
		tree._extendNodeAndAdd.assert_not_called()

	##########################################
	# Tree._extendNodeAndAdd
	##########################################

	def test_extend_node_and_add_001(self):
		level = -3
		node = Mock()
		extended = Mock()

		tree = Tree.__new__(Tree)
		tree._extendNode = MagicMock(return_value = extended)
		tree._addNodes = MagicMock()

		tree._extendNodeAndAdd(level, node)
		tree._extendNode.assert_called_once_with(node)
		tree._addNodes.assert_called_once_with(level, extended)

	##########################################
	# Tree._addNodes
	##########################################

	def test_add_nodes_001(self):
		level = -3
		nodes = list()
		tree = Tree.__new__(Tree)
		tree._addNode = MagicMock()

		tree._addNodes(level, nodes)
		tree._addNode.assert_not_called()

	def test_add_nodes_002(self):
		level = -3
		node1 = Mock()
		nodes = [node1]
		tree = Tree.__new__(Tree)
		tree._addNode = MagicMock()

		tree._addNodes(level, nodes)
		tree._addNode.assert_called_once_with(level, node1)

	def test_add_nodes_003(self):
		level = -3
		node1 = Mock()
		node2 = Mock()
		nodes = [node1, node2]
		tree = Tree.__new__(Tree)
		tree._addNode = MagicMock()

		tree._addNodes(level, nodes)
		self.assertEqual(tree._addNode.mock_calls, [call(level, node1), call(level, node2)])

	##########################################
	# Tree._addNode
	##########################################

	def test_add_node_001(self):
		level = 5
		children = Mock()
		parents = Mock()
		node = Mock()
		node.id = '@I001@'
		node.getChildren = MagicMock(return_value = children)
		node.getParents = MagicMock(return_value = parents)

		tree = Tree.__new__(Tree)
		tree.opened = list()
		tree._openNode = MagicMock()
		tree._addToTree = MagicMock()
		tree._extendNodesAndAdd = MagicMock()

		tree._addNode(level, node)
		tree._openNode.assert_called_once_with(node)
		tree._addToTree.assert_called_once_with(level, node)
		self.assertEqual(tree._extendNodesAndAdd.mock_calls, [call(level+1, children), call(level-1, parents)])

	def test_add_node_002(self):
		level = 5
		node = Mock()
		node.id = '@I001@'
		node.getChildren = MagicMock()
		node.getParents = MagicMock()

		tree = Tree.__new__(Tree)
		tree.opened = [node]
		tree._openNode = MagicMock()
		tree._addToTree = MagicMock()
		tree._extendNodesAndAdd = MagicMock()

		tree._addNode(level, node)
		tree._openNode.assert_not_called()
		tree._addToTree.assert_not_called()
		tree._extendNodesAndAdd.assert_not_called()
		node.getChildren.assert_not_called()
		node.getParents.assert_not_called()

	##########################################
	# Tree._openNode
	##########################################

	def test_open_node_001(self):
		node = Mock()
		tree = Tree.__new__(Tree)
		tree.opened = list()

		tree._openNode(node)
		self.assertEqual(tree.opened, [node])

	def test_open_node_002(self):
		node1 = Mock()
		node2 = Mock()
		tree = Tree.__new__(Tree)
		tree.opened = [node1]

		tree._openNode(node2)
		self.assertEqual(tree.opened, [node1, node2])

	##########################################
	# Tree._extendNodes
	##########################################

	def test_extend_nodes_001(self):
		nodes = list()
		tree = Tree.__new__(Tree)

		extended = tree._extendNodes(nodes)
		self.assertEqual(extended, list())

	def test_extend_nodes_002(self):
		nodes = [Mock()]
		extended = [Mock(), Mock()]

		tree = Tree.__new__(Tree)
		tree._extendNode = MagicMock(return_value = extended)

		returned_extended = tree._extendNodes(nodes)
		self.assertEqual(returned_extended, extended)

	def test_extend_nodes_003(self):
		nodes = [Mock(), Mock()]
		extended1 = [Mock(), Mock()]
		extended2 = [Mock(), Mock(), Mock()]

		tree = Tree.__new__(Tree)
		tree._extendNode = MagicMock(side_effect = [extended1, extended2])

		returned_extended = tree._extendNodes(nodes)
		self.assertEqual(returned_extended, extended1 + extended2)

	##########################################
	# Tree._extendNode
	##########################################
	def test_extend_node_001(self):
		extended = [Mock(), Mock()]
		node = Mock(spec = Union)

		tree = Tree.__new__(Tree)
		tree._extendPerson = MagicMock()
		tree._extendUnion = MagicMock(return_value = extended)

		returned_value = tree._extendNode(node)
		tree._extendPerson.assert_not_called()
		tree._extendUnion.assert_called_once_with(node)
		self.assertEqual(returned_value, extended)

	def test_extend_node_002(self):
		extended = [Mock(), Mock()]
		node = Mock(spec = Person)

		tree = Tree.__new__(Tree)
		tree._extendPerson = MagicMock(return_value = extended)
		tree._extendUnion = MagicMock()

		returned_value = tree._extendNode(node)
		tree._extendPerson.assert_called_once_with(node)
		tree._extendUnion.assert_not_called()
		self.assertEqual(returned_value, extended)

	##########################################
	# Tree._extendPerson
	##########################################
	def test_extend_peson_001(self):
		person = Mock()
		person.isSingle = MagicMock(return_value = True)
		person.getUnions = MagicMock()

		tree = Tree.__new__(Tree)
		tree._openNode = MagicMock()
		tree._extendNodes = MagicMock()

		extended = tree._extendPerson(person)
		person.isSingle.assert_called_once_with()
		person.getUnions.assert_not_called()
		tree._openNode.assert_not_called()
		tree._extendNodes.assert_not_called()
		self.assertEqual(extended, [person])

	def test_extend_peson_002(self):
		unions = Mock()
		person = Mock()
		person.isSingle = MagicMock(return_value = False)
		person.getUnions = MagicMock(return_value = unions)

		extended = Mock()
		tree = Tree.__new__(Tree)
		tree._openNode = MagicMock()
		tree._extendNodes = MagicMock(return_value = extended)

		returned_extended = tree._extendPerson(person)
		person.isSingle.assert_called_once_with()
		person.getUnions.assert_called_once_with()
		tree._openNode.assert_called_once_with(person)
		tree._extendNodes.assert_called_once_with(unions)
		self.assertEqual(returned_extended, extended)

	##########################################
	# Tree._extendUnion
	##########################################

	'''
	Test when there is nothing to dequeu
	'''
	@patch("src.unique_queue.unique_queue.__new__")
	def test_extend_union_001(self, class_queue):
		all = []

		union = Mock()
		union.getUnions = MagicMock()

		queue = Mock()
		queue.isEmpty = MagicMock(return_value = True)
		queue.pop = MagicMock()
		queue.pushList = MagicMock()
		queue.getAll = MagicMock(return_value = all)

		class_queue.return_value = queue

		tree = Tree.__new__(Tree)

		# Checks
		returned_value = tree._extendUnion(union)
		queue.isEmpty.assert_called_once_with()
		queue.pop.assert_not_called()
		union.getUnions.assert_not_called()
		queue.pushList.assert_not_called()
		queue.getAll.assert_called_once_with()
		self.assertEqual(returned_value, all)

	'''
	Test when the queue has elements
	'''
	@patch("src.unique_queue.unique_queue.__new__")
	def test_extend_union_002(self, class_queue):
		unions = []

		union = Mock()
		union.getUnions = MagicMock(return_value = unions)
		all = Mock()

		queue = Mock()
		queue.isEmpty = MagicMock(side_effect = [False, True])
		queue.pop = MagicMock(return_value = union)
		queue.pushList = MagicMock()
		queue.getAll = MagicMock(return_value = all)

		class_queue.return_value = queue

		tree = Tree.__new__(Tree)

		# Checks
		returned_value = tree._extendUnion(union)
		self.assertEqual(queue.isEmpty.mock_calls, [call(), call()])
		queue.pop.assert_called_once_with()
		union.getUnions.assert_called_once_with()
		queue.pushList.assert_called_once_with(unions)
		queue.getAll.assert_called_once_with()
		self.assertEqual(returned_value, all)

	##########################################
	# Tree._createEdges
	##########################################

	def test_create_edges_001(self):
		unions = list()
		edges = list()

		tree = Tree.__new__(Tree)
		tree._createEdgesFromNode = MagicMock()

		return_value = tree._createEdges(unions)
		tree._createEdgesFromNode.assert_not_called()
		self.assertEqual(return_value, edges)

	def test_create_edges_002(self):
		union1 = Mock()
		union2 = Mock()
		unions = [union1, union2]

		edges_union1 = [Mock(), Mock()]
		edges_union2 = [Mock()]

		tree = Tree.__new__(Tree)
		tree._createEdgesFromNode = MagicMock(side_effect = [edges_union1, edges_union2])

		return_value = tree._createEdges(unions)
		self.assertEqual(tree._createEdgesFromNode.mock_calls, [call(union1), call(union2)])
		self.assertEqual(return_value, edges_union1 + edges_union2)

	##########################################
	# Tree._createEdgesFromNode
	##########################################

	@patch("src.tree.print", create=True)
	def test_create_edges_from_node_001(self, mock_print):
		node = Mock()
		node.id = '@F0002@'

		tree = Tree.__new__(Tree)
		tree._createEdgesToNodes = MagicMock()
		tree.opened = list()

		return_value = tree._createEdgesFromNode(node)
		mock_print.assert_called_with('Element @F0002@ not processed. Check your ged file for inconsistent data.')
		tree._createEdgesToNodes.assert_not_called()
		self.assertEqual(return_value, list())

	@patch("src.tree.print", create=True)
	def test_create_edges_from_node_002(self, mock_print):
		children = Mock()
		node = Mock()
		node.id = '@F0002@'
		node.getChildren = MagicMock(return_value = children)

		edges = Mock()
		tree = Tree.__new__(Tree)
		tree._createEdgesToNodes = MagicMock(return_value = edges)
		tree.opened = [node]

		return_value = tree._createEdgesFromNode(node)
		mock_print.assert_not_called()
		tree._createEdgesToNodes.assert_called_once_with(node, children)
		self.assertEqual(return_value, edges)

	##########################################
	# Tree._createEdgesToNodes
	##########################################

	def test_create_edges_to_nodes_001(self):
		tree = Tree.__new__(Tree)
		tree._createEdgeToNode = MagicMock()

		start = Mock()
		nodes = list()
		edges = list()

		return_value = tree._createEdgesToNodes(start, nodes)
		tree._createEdgeToNode.assert_not_called()
		self.assertEqual(return_value, edges)

	def test_create_edges_to_nodes_002(self):
		edge1 = Mock()
		edge2 = Mock()
		edges = [edge1, edge2]
		tree = Tree.__new__(Tree)
		tree._createEdgeToNode = MagicMock(side_effect = [[edge1], [edge2]])

		start = Mock()
		node1 = Mock()
		node2 = Mock()
		nodes = [node1, node2]

		return_value = tree._createEdgesToNodes(start, nodes)
		self.assertEqual(tree._createEdgeToNode.mock_calls, [call(start, node1), call(start, node2)])
		self.assertEqual(return_value, edges)

	##########################################
	# Tree._createEdgeToNode
	##########################################

	@patch("src.tree.print", create=True)
	@patch("src.edge.Edge.__new__")
	def test_create_edge_to_node_001(self, mock_edge, mock_print):
		start = Mock()
		node = Mock()
		node.id = '@I0002@'

		tree = Tree.__new__(Tree)
		tree.opened = list()

		return_value = tree._createEdgeToNode(start, node)
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

		return_value = tree._createEdgeToNode(start, node)
		mock_print.assert_not_called()
		mock_edge.assert_called_once_with(ANY, start.id, node.id)
		self.assertEqual(return_value, [edge])

	##########################################
	# Tree._getStartingNode
	##########################################

	def test_get_starting_person_001(self):
		# Setup people
		person1 = None
		people = dict()

		# Setup Tree
		tree = Tree.__new__(Tree)

		# Actual test
		returned_person = tree._getStartingNode(people)
		self.assertEqual(returned_person, person1)

	def test_get_starting_person_002(self):
		# Setup people
		id1 = '@I0001234@'
		person1 = Mock()
		people = {id1:person1}

		# Setup Tree
		tree = Tree.__new__(Tree)

		# Actual test
		returned_person = tree._getStartingNode(people)
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
		returned_person = tree._getStartingNode(people)
		self.assertEqual(returned_person, person2)

	##########################################
	# Tree._addToTree
	##########################################

	@patch("src.tree_level.TreeLevel.__new__")
	def test_add_to_tree_001(self, class_tree_level):
		node = Mock()

		level_1 = Mock()
		level_1.append = MagicMock()
		class_tree_level.return_value = level_1

		tree = Tree.__new__(Tree)
		tree.levels = dict()

		tree._addToTree(1, node)
		class_tree_level.assert_called_once()
		level_1.append.assert_called_once_with(node)

	@patch("src.tree_level.TreeLevel.__new__")
	def test_add_to_tree_002(self, class_tree_level):
		node = Mock()

		level_1 = Mock()
		level_1.append = MagicMock()

		tree = Tree.__new__(Tree)
		tree.levels = {1: level_1}

		tree._addToTree(1, node)
		class_tree_level.assert_not_called()
		level_1.append.assert_called_once_with(node)

	##########################################
	# Tree._levelsToNodes
	##########################################

	def test_levels_to_nodes_001(self):
		node1 = Mock()
		node2 = Mock()
		node3 = Mock()

		tree = Tree.__new__(Tree)
		tree.levels = {1: node1, 2: node2, 3:node3}

		return_value = tree._levelsToNodes()
		self.assertEqual(return_value, [node3, node2, node1])

	def test_levels_to_nodes_002(self):
		node1 = Mock()
		node2 = Mock()
		node3 = Mock()

		tree = Tree.__new__(Tree)
		tree.levels = {2: node2, 1: node1, 3:node3}

		return_value = tree._levelsToNodes()
		self.assertEqual(return_value, [node3, node2, node1])

	def test_levels_to_nodes_003(self):
		node1 = Mock()
		node2 = Mock()
		node3 = Mock()

		tree = Tree.__new__(Tree)
		tree.levels = {3: node3, 2: node2, 1: node1}

		return_value = tree._levelsToNodes()
		self.assertEqual(return_value, [node3, node2, node1])

if __name__ == '__main__':
	unittest.main()
