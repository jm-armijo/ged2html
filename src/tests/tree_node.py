import unittest
from unittest.mock import MagicMock, Mock
from ..html import HTMLGenerator
from ..tree_node import TreeNode

class TestTreeNode(unittest.TestCase):

	##########################################
	# TreeNode.init
	##########################################

	def test_init_001(self):
		node = Mock()
		tree_node = TreeNode(node)
		self.assertEqual(tree_node.node, node)

	def test_to_html_001(self):
		# Mock node
		html = '<div>X</div>'
		node = Mock()
		node.to_html = MagicMock(return_value = html)

		# Mock HTML Generator
		wrapped = "<div>"+html+"</div>"
		HTMLGenerator.wrap = MagicMock(return_value = wrapped)

		# Mock TreeNode
		tree_node = TreeNode.__new__(TreeNode)
		tree_node.node = node

		# Actual test
		return_value = tree_node.to_html()
		node.to_html.assert_called_once_with()
		HTMLGenerator.wrap.assert_called_once_with(tree_node, html)
		self.assertEqual(return_value, wrapped)

if __name__ == '__main__':
	unittest.main()
