import unittest
from unittest.mock import patch
from unittest.mock import Mock
from node import Node 

class TestLine(unittest.TestCase):
	def test_init_001(self):
		level = 100
		key = 'key'
		value = 'value'

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, [])

	def test_init_002(self):
		level = -103
		key = 'this is a key'
		value = 'and this is a value'

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, [])

	def test_init_003(self):
		level = 0
		key = 'key'
		value = ''

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, [])

	def test_init_004(self):
		level = 0
		key = 'key'
		value = ''

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, [])

	'''
	Inserts an attribute at the root level (depth 1)
	'''
	def test_add_node_001(self):
		# Setup Node
		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value = '@I000123@'
		node_obj.children = list()

		# Setup new attribute
		attribute = Mock()
		attribute.level = 1

		# Actual test
		node_obj.addNode(attribute)
		self.assertEqual(node_obj.children[-1], attribute)

	'''
	Inserts an attribute at depth 3
	'''
	def test_add_node_002(self):
		# Setup tree
		lvl2 = Node.__new__(Node)
		lvl2.level = 2
		lvl2.children = list()

		lvl1 = Node.__new__(Node)
		lvl1.level = 1
		lvl1.children = [lvl2]

		root_obj = Node.__new__(Node)
		root_obj.level = 0
		root_obj.children = [lvl1]

		# Setup new attribute
		attribute = Mock()
		attribute.level = 3

		# Actual test
		root_obj.addNode(attribute)
		self.assertEqual(root_obj.children[-1].children[-1].children[-1], attribute)

	'''
	Gets an attribute from index 0
	'''
	def test_get_item_001(self):
		# Setup Node
		attribute = Mock()
		node_obj = Node.__new__(Node)
		node_obj.children = [attribute, Mock()]

		# Actual test
		self.assertEqual(node_obj[0], attribute)

	'''
	Gets an attribute from index 1
	'''
	def test_get_item_002(self):
		# Setup Node
		attribute = Mock()
		node_obj = Node.__new__(Node)
		node_obj.children = [Mock(), attribute]

		# Actual test
		self.assertEqual(node_obj[1], attribute)

	'''
	Gets an attribute from empty list
	'''
	def test_get_item_003(self):
		# Setup Node
		node_obj = Node.__new__(Node)
		node_obj.children = list()

		# Actual test
		self.assertRaises(IndexError, node_obj.__getitem__, 1)

	'''
	Casts childrenless node into string
	'''
	def test_str_001(self):
		# Setup Node
		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = list()

		# Actual test
		expected = 'INDI : @I000123@'
		self.assertEqual(str(node_obj), expected)

	'''
	Casts node with 1 child into string
	'''
	def test_str_002(self):
		# Setup Node
		child_obj = Node.__new__(Node)
		child_obj.level = 1
		child_obj.key   = "KEY"
		child_obj.value  = 'Value'
		child_obj.children = list()

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = [child_obj]

		# Actual test
		expected = 'INDI : @I000123@\n KEY : Value'
		self.assertEqual(str(node_obj), expected)

	'''
	Casts node with 2 children into string
	'''
	def test_str_003(self):
		# Setup Node
		child1_obj = Node.__new__(Node)
		child1_obj.level = 1
		child1_obj.key   = "KEY1"
		child1_obj.value  = 'Value1'
		child1_obj.children = list()

		child2_obj = Node.__new__(Node)
		child2_obj.level = 1
		child2_obj.key   = "KEY2"
		child2_obj.value  = 'Value2'
		child2_obj.children = list()

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = [child1_obj, child2_obj]

		# Actual test
		expected = 'INDI : @I000123@\n KEY1 : Value1\n KEY2 : Value2'
		self.assertEqual(str(node_obj), expected)

	'''
	Casts node with 1 child and 2 granchild into string
	'''
	def test_str_004(self):
		# Setup Node
		grand_child1_obj = Node.__new__(Node)
		grand_child1_obj.level = 2
		grand_child1_obj.key   = "KEY1"
		grand_child1_obj.value  = 'Value1'
		grand_child1_obj.children = list()

		grand_child2_obj = Node.__new__(Node)
		grand_child2_obj.level = 2
		grand_child2_obj.key   = "KEY2"
		grand_child2_obj.value  = 'Value2'
		grand_child2_obj.children = list()

		child_obj = Node.__new__(Node)
		child_obj.level = 1
		child_obj.key   = "KEY"
		child_obj.value  = 'Value'
		child_obj.children = [grand_child1_obj, grand_child2_obj]

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = [child_obj]

		# Actual test
		expected = 'INDI : @I000123@\n KEY : Value\n  KEY1 : Value1\n  KEY2 : Value2'
		self.assertEqual(str(node_obj), expected)

if __name__ == '__main__':
	unittest.main()
