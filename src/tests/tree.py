import unittest
from unittest.mock import Mock
from ..tree import Tree

class TestTree(unittest.TestCase):

	##########################################
	# Tree.init
	##########################################

	def test_init_001(self):
		tree = Tree()
		tree.nodes = dict()
		self.assertEqual(tree.nodes, dict())

	##########################################
	# Tree.add
	##########################################

	def test_add_001(self):
		node1 = Mock()
		node2 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = {1:[node1]}
		tree.add(1, node2)

		self.assertEqual(tree.nodes, {1: [node1, node2]})

	def test_add_002(self):
		node1 = Mock()

		tree = Tree.__new__(Tree)
		tree.nodes = dict()
		tree.add(1, node1)

		self.assertEqual(tree.nodes, {1: [node1]})

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
