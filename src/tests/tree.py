import unittest
from unittest.mock import Mock, patch, MagicMock, call
from ..tree import Tree

class TestTree(unittest.TestCase):

	##########################################
	# Tree.init
	##########################################

	@patch("src.tree.Tree._getStartingPerson")
	@patch("src.tree.Tree._addPerson")
	def test_init_001(self, mock_add, mock_start):
		person = Mock()
		mock_start.return_value = person

		people = Mock()
		tree = Tree(people)

		self.assertEqual(tree.nodes, dict())
		self.assertEqual(tree.people, people)
		mock_start.assert_called_with()
		mock_add.assert_called_with(0, person)

	@patch("src.tree.Tree._getStartingPerson")
	@patch("src.tree.Tree._addPerson")
	def test_init_002(self, mock_add, mock_start):
		person = None
		mock_start.return_value = person

		people = Mock()
		tree = Tree(people)

		self.assertEqual(tree.nodes, dict())
		self.assertEqual(tree.people, people)
		mock_start.assert_called_with()
		mock_add.assert_called_with(0, person)

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
	# Tree._appendOnLevel
	##########################################

	def test_append_on_level001(self):
		node1 = Mock()
		node2 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = {1:[node1]}
		tree._appendOnLevel(1, node2)

		self.assertEqual(tree.nodes, {1: [node1, node2]})

	def test_append_on_level002(self):
		node1 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = dict()
		tree._appendOnLevel(1, node1)

		self.assertEqual(tree.nodes, {1: [node1]})

	##########################################
	# Tree._addPerson
	##########################################

	def test_create_node_on_tree_001(self):
		# Setup Person
		unions = []
		person = Mock()
		person.unions = unions

		# Setup Tree
		tree = Tree.__new__(Tree)
		tree._appendOnLevel = MagicMock()
		tree._addUnions = MagicMock()

		# Actual test
		level = 5
		tree._addPerson(level, person)
		tree._appendOnLevel.assert_called_with(level, person)
		tree._addUnions.assert_not_called()

	def test_create_node_on_tree_002(self):
		# Setup Person
		union1 = Mock()
		unions = [union1]
		person = Mock()
		person.unions = unions

		# Setup Tree
		tree = Tree.__new__(Tree)
		tree._appendOnLevel = MagicMock()
		tree._addUnions = MagicMock()

		# Actual test
		level = 5
		tree._addPerson(level, person)
		tree._appendOnLevel.assert_not_called()
		tree._addUnions.assert_called_with(level, unions)

	def test_create_node_on_tree_003(self):
		# Setup Person
		union1 = Mock()
		union2 = Mock()
		unions = [union1, union2]
		person = Mock()
		person.unions = unions

		# Setup Tree
		tree = Tree.__new__(Tree)
		tree._appendOnLevel = MagicMock()
		tree._addUnions = MagicMock()

		# Actual test
		level = 5
		tree._addPerson(level, person)
		tree._appendOnLevel.assert_not_called()
		tree._addUnions.assert_called_with(level, unions)

	##########################################
	# Tree._addUnions
	##########################################

	def test_add_unions_001(self):
		# Setup Tree
		tree = Tree.__new__(Tree)
		tree._appendOnLevel = MagicMock()
		tree._addChildren = MagicMock()

		# Setup Unions
		level = 5
		union1 = Mock()
		union2 = Mock()

		union1.children = Mock()
		union2.children = Mock()

		unions = [union1, union2]

		# Actual test
		tree._addUnions(level, unions)

		self.assertEqual(tree._appendOnLevel.call_count, len(unions))
		self.assertEqual(tree._appendOnLevel.mock_calls, [call(level, union1), call(level, union2)])

		self.assertEqual(tree._addChildren.call_count, len(unions))
		self.assertEqual(tree._addChildren.mock_calls, [call(level+1, union1.children), call(level+1, union2.children)])

	def test_add_unions_002(self):
		# Setup Tree
		tree = Tree.__new__(Tree)
		tree._appendOnLevel = MagicMock()
		tree._addChildren = MagicMock()

		# Setup Unions
		level = 5
		unions = []

		# Actual test
		tree._addUnions(level, unions)

		tree._appendOnLevel.assert_not_called()
		tree._addChildren.assert_not_called()

	##########################################
	# Tree._addChildren
	##########################################

	def test_create_children_nodes_001(self):
		# Setup
		level = 5
		child1 = Mock()
		child2 = Mock()
		child3 = Mock()
		children = [child1, child2, child3]

		tree = Tree.__new__(Tree)
		tree._addPerson = MagicMock()

		# Actual test
		tree._addChildren(level, children)
		self.assertEqual(tree._addPerson.call_count, len(children))
		self.assertEqual(tree._addPerson.mock_calls, [call(level, child1), call(level, child2), call(level, child3)])

	def test_create_children_nodes_002(self):
		# Setup
		level = 5
		children = []

		tree = Tree.__new__(Tree)
		tree._addPerson = MagicMock()

		# Actual test
		tree._addChildren(level, children)
		self.assertEqual(tree._addPerson.call_count, len(children))

	def test_create_children_nodes_003(self):
		# Setup
		level = -15
		child1 = Mock()
		child2 = Mock()
		child3 = Mock()
		children = [child1, child2, child3]

		tree = Tree.__new__(Tree)
		tree._addPerson = MagicMock()

		# Actual test
		tree._addChildren(level, children)
		self.assertEqual(tree._addPerson.call_count, len(children))
		self.assertEqual(tree._addPerson.mock_calls, [call(level, child1), call(level, child2), call(level, child3)])

	def test_create_children_nodes_004(self):
		# Setup
		level = 0
		child1 = Mock()
		children = [child1]

		tree = Tree.__new__(Tree)
		tree._addPerson = MagicMock()

		# Actual test
		tree._addChildren(level, children)
		self.assertEqual(tree._addPerson.call_count, len(children))
		self.assertEqual(tree._addPerson.mock_calls, [call(level, child1)])

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
