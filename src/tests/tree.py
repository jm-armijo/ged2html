import unittest
from unittest.mock import Mock, patch, MagicMock, call
from ..tree import Tree

class TestTree(unittest.TestCase):

	##########################################
	# Tree.init
	##########################################

	@patch("src.tree.Tree._getStartingPerson")
	@patch("src.tree.Tree._extendNodesAndAdd")
	def test_init_001(self, mock_add, mock_start):
		person = Mock()
		mock_start.return_value = person

		people = Mock()
		tree = Tree(people)

		self.assertEqual(tree.nodes, dict())
		self.assertEqual(tree.opened, list())
		self.assertEqual(tree.people, people)

		mock_start.assert_called_with()
		mock_add.assert_called_with(0, [person])

	##########################################
	# Tree._getStartingPerson
	##########################################

	def test_get_starting_person_001(self):
		# Setup people
		person1 = None
		people = dict()

		# Setup Tree
		tree = Tree.__new__(Tree)
		tree.people = people

		# Actual test
		returned_person = tree._getStartingPerson()
		self.assertEqual(returned_person, person1)

	def test_get_starting_person_002(self):
		# Setup people
		id1 = '@I0001234@'
		person1 = Mock()
		people = {id1:person1}

		# Setup Tree
		tree = Tree.__new__(Tree)
		tree.people = people

		# Actual test
		returned_person = tree._getStartingPerson()
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
		tree.people = people

		# Actual test
		returned_person = tree._getStartingPerson()
		self.assertEqual(returned_person, person2)

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
		node = Mock()
		node.id = '@I001@'

		tree = Tree.__new__(Tree)
		tree.opened = [node.id]
		tree._addToTree = MagicMock()
		tree._getNodeChildren = MagicMock()
		tree._getNodeParents = MagicMock()
		tree._addNodes = MagicMock()

		tree._addNode(level, node)
		tree._addToTree.assert_not_called()
		tree._getNodeChildren.assert_not_called()
		tree._getNodeParents.assert_not_called()
		tree._addNodes.assert_not_called()

	def test_add_node_002(self):
		# Setup children and parents
		children = Mock()
		parents = Mock()

		# Setup node
		level = 5
		node = Mock()
		node.id = '@I001@'
		node.getChildren = MagicMock(return_value = children)
		node.getParents = MagicMock(return_value = parents)

		# Setup tree
		tree = Tree.__new__(Tree)
		tree.opened = list()
		tree._addToTree = MagicMock()
		tree._extendNodesAndAdd = MagicMock()

		tree._addNode(level, node)
		self.assertTrue(node.id in tree.opened)
		tree._addToTree.assert_called_once_with(level, node)
		self.assertEqual(tree._extendNodesAndAdd.mock_calls, [call(level+1, children), call(level-1, parents)])

	##########################################
	# Tree._addToTree
	##########################################

	def test_add_to_tree_001(self):
		node1 = Mock()
		node2 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = {1:[node1]}
		tree._addToTree(1, node2)

		self.assertEqual(tree.nodes, {1: [node1, node2]})

	def test_add_to_tree_002(self):
		node1 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = dict()
		tree._addToTree(1, node1)

		self.assertEqual(tree.nodes, {1: [node1]})

	##########################################
	# Tree._extendNodesAndAdd
	##########################################

	def test_extend_nodes_and_add_001(self):
		level = 4
		nodes = Mock()
		extended = Mock()

		tree = Tree.__new__(Tree)
		tree._extendNodes = MagicMock(return_value = extended)
		tree._addNodes = MagicMock()

		tree._extendNodesAndAdd(level, nodes)
		tree._addNodes.assert_called_once_with(level, extended)

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

	# Returns unions of all spouses of a union, and of their spouses
	# Ex. Given:
	# u1{ X & J}
	#   u2{ J & F }
	#       u3{ F & A }
	#           u4{ A & H }
	# Returns: u1, u2, u3

	def test_extend_node_001(self):
		# Create Person and Union objects
		personX = Mock()
		personJ = Mock()
		personF = Mock()
		personA = Mock()
		personH = Mock()

		personX.id = '@I001@'
		personJ.id = '@I002@'
		personF.id = '@I003@'
		personA.id = '@I004@'
		personH.id = '@I005@'

		personX.unions = list()
		personJ.unions = list()
		personF.unions = list()
		personA.unions = list()
		personH.unions = list()

		union1 = Mock()
		union2 = Mock()
		union3 = Mock()
		union4 = Mock()

		union1.id = '@F0001@'
		union2.id = '@F0002@'
		union3.id = '@F0003@'
		union4.id = '@F0004@'

		# Link Union and Person objects
		union1.spouse1 = personX
		union1.spouse2 = personJ
		personX.unions.append(union1)
		personJ.unions.append(union1)

		union2.spouse1 = personJ
		union2.spouse2 = personF
		personJ.unions.append(union2)
		personF.unions.append(union2)

		union3.spouse1 = personF
		union3.spouse2 = personA
		personF.unions.append(union3)
		personA.unions.append(union3)

		union4.spouse1 = personA
		union4.spouse2 = personH
		personA.unions.append(union4)
		personH.unions.append(union4)

		# Setup parser
		parser = Tree.__new__(Tree)

		# Actual test
		unions = parser._extendNode(union3)
		self.assertEqual(len(unions), 4)
		self.assertTrue(union1 in unions)
		self.assertTrue(union2 in unions)
		self.assertTrue(union3 in unions)
		self.assertTrue(union3 in unions)

	##########################################
	# Tree._getLevels
	##########################################

	def test_get_levels_001(self):
		tree = Tree.__new__(Tree)
		tree.nodes = {1:[], 2:[], 3:[]}
		levels = tree._getLevels()

		self.assertEqual(levels, [1,2,3])

	def test_get_levels_002(self):
		tree = Tree.__new__(Tree)
		tree.nodes = {-4:[], 3:[], 0:[]}
		levels = tree._getLevels()

		self.assertEqual(levels, [-4,0,3])

	def test_get_levels_003(self):
		tree = Tree.__new__(Tree)
		tree.nodes = {}
		levels = tree._getLevels()

		self.assertEqual(levels, [])

	def test_get_levels_004(self):
		tree = Tree.__new__(Tree)
		tree.nodes = {1000:[], -3000000:[], 1:[], 5:[], 9:[]}
		levels = tree._getLevels()

		self.assertEqual(levels, [-3000000, 1, 5, 9, 1000])

	def test_get_levels_005(self):
		tree = Tree.__new__(Tree)
		tree.nodes = {1:[], 'k':[]}
		self.assertRaises(TypeError, tree._getLevels)

if __name__ == '__main__':
	unittest.main()
