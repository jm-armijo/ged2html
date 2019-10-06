import unittest
from unittest.mock import MagicMock, Mock, patch, ANY
from ..html import HTMLGenerator
from ..person import Person
from ..tree_node import TreeNode
from ..union_extended import UnionExtended

class TestTreeNode(unittest.TestCase):

    ##########################################
    # TreeNode.init
    ##########################################

    def test_init_001(self):
        node = Mock(spec=Person)
        node.get_unions = MagicMock()
        node.is_single = MagicMock(return_value = True)

        tree_node = TreeNode(node)
        tree_node.unions = list()
        tree_node.people = list()

        self.assertEqual(tree_node.node, node)

    @patch("src.union_extended.UnionExtended.__new__")
    def test_init_002(self, class_union_extended):
        union = Mock()
        unions = [union]

        node = Mock()
        node.get_unions = MagicMock(return_value = unions)
        node.is_single = MagicMock(return_value = True)

        union_extended = Mock()
        class_union_extended.return_value = union_extended

        tree_node = TreeNode(node)
        tree_node.unions = list()
        tree_node.people = list()

        class_union_extended.assert_called_once_with(ANY, unions)
        self.assertEqual(tree_node.node, union_extended)

    ##########################################
    # TreeNode.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = [Mock()]
        node = Mock()
        node.get_unions = MagicMock(return_value = unions)

        tree_node = TreeNode.__new__(TreeNode)
        tree_node.node = node

        expected = unions
        actual = tree_node.get_unions()
        self.assertEqual(expected, actual)

    ##########################################
    # TreeNode.get_spouses
    ##########################################

    def test_get_spouses_001(self):
        spouses = [Mock(), Mock()]
        node = Mock()
        node.get_spouses = MagicMock(return_value = spouses)

        tree_node = TreeNode.__new__(TreeNode)
        tree_node.node = node

        expected = spouses
        actual = tree_node.get_spouses()
        self.assertEqual(expected, actual)

    ##########################################
    # TreeNode.get_children
    ##########################################

    def test_get_children_001(self):
        children = [Mock(), Mock()]
        node = Mock()
        node.get_children = MagicMock(return_value = children)

        tree_node = TreeNode.__new__(TreeNode)
        tree_node.node = node

        expected = children
        actual = tree_node.get_children()
        self.assertEqual(expected, actual)

    ##########################################
    # TreeNode.get_parents
    ##########################################

    def test_get_parents_001(self):
        parents = [Mock(), Mock()]
        node = Mock()
        node.get_parents = MagicMock(return_value = parents)

        tree_node = TreeNode.__new__(TreeNode)
        tree_node.node = node

        expected = parents
        actual = tree_node.get_parents()
        self.assertEqual(expected, actual)

    ##########################################
    # TreeNode.to_html
    ##########################################

    def test_to_html_001(self):
        # Mock node
        html = '<div>X</div>'
        node = Mock()
        node.to_html = MagicMock(return_value = html)

        # Mock HTML Generator
        wrapped = "<div>"+html+"</div>"
        HTMLGenerator.wrap_instance = MagicMock(return_value = wrapped)

        # Mock TreeNode
        tree_node = TreeNode.__new__(TreeNode)
        tree_node.node = node

        # Actual test
        return_value = tree_node.to_html()
        node.to_html.assert_called_once_with()
        HTMLGenerator.wrap_instance.assert_called_once_with(tree_node, html)
        self.assertEqual(return_value, wrapped)

if __name__ == '__main__':
    unittest.main()
