import unittest
from unittest.mock import patch
from unittest.mock import Mock

from ..node import Node

class TestNode(unittest.TestCase):
	def test_init_001(self):
		level = 100
		key = 'key'
		value = 'value'

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, {})

	def test_init_002(self):
		level = -103
		key = 'this is a key'
		value = 'and this is a value'

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, {})

	def test_init_003(self):
		level = 0
		key = 'key'
		value = ''

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, {})

	def test_init_004(self):
		level = 0
		key = 'key'
		value = ''

		node = Node(level, key, value)
	
		self.assertEqual(node.level, level)
		self.assertEqual(node.key,   key)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, {})

	'''
	Inserts an attribute on a given parent node
	'''
	@patch("src.node.Node.__init__")
	@patch("src.node.Node.appendAttribute")
	def test_add_node_001(self, mock_append, mock_init):
		mock_init.return_value = None

		# Setup attribute's values
		level = 1
		key = 'KEY1'
		value = 'Value'

		node_obj = Node.__new__(Node)
		node_obj.addNode(level, key, value)

		mock_init.assert_called_with(level, key, value)

		mock_append.assert_called()
		self.assertTrue(isinstance(mock_append.call_args[0][0], Node))

	@patch("src.node.Node.pickParent")
	def test_append_attribute_001(self, mock_pick):
		# Mock pickParent
		parent = Mock()
		parent.children = dict()
		mock_pick.return_value = parent

		# Setup new attribute
		attribute = Mock()
		attribute.level = 1
		attribute.key = 'KEY1'
		attribute.value = 'Value'

		# Actual test
		node_obj = Node.__new__(Node)
		node_obj.appendAttribute(attribute)
		self.assertEqual(parent.last_child, 'KEY1')
		self.assertEqual(parent.children['KEY1'].level, attribute.level)
		self.assertEqual(parent.children['KEY1'].key,   attribute.key)
		self.assertEqual(parent.children['KEY1'].value, attribute.value)

	'''
	Inserts duplicated attribute with empty value
	'''
	@patch("src.node.Node.pickParent")
	def test_append_attribute_002(self, mock_pick):
		# Setup an attribute
		attribute = Mock()
		attribute.level = 1
		attribute.key = 'KEY1'
		attribute.value = 'VALUE1'

		# Setup dup attribute with empty value
		dup_attribute = Mock()
		dup_attribute.level = 1
		dup_attribute.key = 'KEY1'
		dup_attribute.value = ''

		parent = Mock()
		parent.children = {'KEY1':attribute}
		mock_pick.return_value = parent

		# Actual test
		node_obj = Node.__new__(Node)
		node_obj.appendAttribute(dup_attribute)
		self.assertEqual(parent.last_child,'KEY1')

		# Attribute is not replaced
		self.assertEqual(parent.children['KEY1'].value, attribute.value)

	'''
	Inserts duplicated attribute with longer value
	'''
	@patch("src.node.Node.pickParent")
	def test_append_attribute_003(self, mock_pick):
		# Setup an attribute
		attribute = Mock()
		attribute.level = 1
		attribute.key = 'KEY1'
		attribute.value = ''

		# Setup dup attribute with empty value
		dup_attribute = Mock()
		dup_attribute.level = 1
		dup_attribute.key = 'KEY1'
		dup_attribute.value = 'This is a long value'

		# Setup parent node
		parent = Mock()
		parent.children = {'KEY1':attribute}
		mock_pick.return_value = parent

		# Actual test
		node_obj = Node.__new__(Node)
		node_obj.appendAttribute(dup_attribute)
		self.assertEqual(parent.last_child,'KEY1')

		# Attribute is replaced
		self.assertEqual(parent.children['KEY1'].value, dup_attribute.value)

	'''
	Get parent for attribute at depth 1
	'''
	def test_pick_parent_001(self):
		# Setup Node
		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value = '@I000123@'
		node_obj.children = dict()

		# Setup new attribute
		attribute = Mock()
		attribute.level = 1
		attribute.key = 'KEY1'

		# Actual test
		parent = node_obj.pickParent(attribute)
		self.assertEqual(parent, node_obj)

	'''
	Get parent for attribute at depth 3
	'''
	def test_pick_parent_002(self):
		# Setup tree
		node_lvl2 = Node.__new__(Node)
		node_lvl2.key = 'KEY2'
		node_lvl2.level = 2
		node_lvl2.children = dict()
		node_lvl2.last_child = None

		node_lvl1 = Node.__new__(Node)
		node_lvl1.key = 'KEY1'
		node_lvl1.level = 1
		node_lvl1.children = {'KEY2':node_lvl2}
		node_lvl1.last_child = 'KEY2'

		root_obj = Node.__new__(Node)
		root_obj.key = 'KEY0'
		root_obj.level = 0
		root_obj.children = {'KEY1':node_lvl1}
		root_obj.last_child = 'KEY1'

		# Setup new attribute
		attribute = Mock()
		attribute.key = 'KEY3'
		attribute.level = 3

		# Actual test
		parent = root_obj.pickParent(attribute)
		self.assertEqual(parent, node_lvl2)

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
		node_obj.children = dict()

		# Actual test
		self.assertRaises(KeyError, node_obj.__getitem__, 1)

	'''
	Casts childrenless node into string
	'''
	def test_str_001(self):
		# Setup Node
		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = dict()

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
		child_obj.children = dict()

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = {'KEY':child_obj}

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
		child1_obj.children = dict()

		child2_obj = Node.__new__(Node)
		child2_obj.level = 1
		child2_obj.key   = "KEY2"
		child2_obj.value  = 'Value2'
		child2_obj.children = dict()

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = {'KEY1':child1_obj, 'KEY2':child2_obj}

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
		grand_child1_obj.children = dict()

		grand_child2_obj = Node.__new__(Node)
		grand_child2_obj.level = 2
		grand_child2_obj.key   = "KEY2"
		grand_child2_obj.value  = 'Value2'
		grand_child2_obj.children = dict()

		child_obj = Node.__new__(Node)
		child_obj.level = 1
		child_obj.key   = "KEY"
		child_obj.value  = 'Value'
		child_obj.children = {'KEY1':grand_child1_obj, 'KEY2':grand_child2_obj}

		node_obj = Node.__new__(Node)
		node_obj.level = 0
		node_obj.key   = "INDI"
		node_obj.value  = '@I000123@'
		node_obj.children = {'KEY':child_obj}

		# Actual test
		expected = 'INDI : @I000123@\n KEY : Value\n  KEY1 : Value1\n  KEY2 : Value2'
		self.assertEqual(str(node_obj), expected)

if __name__ == '__main__':
	unittest.main()
