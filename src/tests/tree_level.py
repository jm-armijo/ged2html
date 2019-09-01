import unittest
from unittest.mock import MagicMock, Mock, patch, ANY
from ..html import HTMLGenerator
from ..tree_level import TreeLevel

class TestTreeLevel(unittest.TestCase):

    ##########################################
    # TreeLevel.init
    ##########################################

    def test_init_001(self):
        tree_level = TreeLevel()
        self.assertEqual(tree_level.nodes, list())

    ##########################################
    # TreeLevel.append
    ##########################################

    @patch("src.tree_node.TreeNode.__new__")
    def test_append_001(self, class_treenode):
        node = Mock()
        tree_node = Mock()
        class_treenode.return_value = tree_node

        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = list()

        tree_level.append(node)
        class_treenode.assert_called_once_with(ANY, node)
        self.assertEqual(tree_level.nodes, [tree_node])

    @patch("src.tree_node.TreeNode.__new__")
    def test_append_002(self, class_treenode):
        node = Mock()
        tree_node1 = Mock()
        tree_node2 = Mock()
        class_treenode.return_value = tree_node2

        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = [tree_node1]

        tree_level.append(node)
        class_treenode.assert_called_once_with(ANY, node)
        self.assertEqual(tree_level.nodes, [tree_node1, tree_node2])

    ##########################################
    # TreeLevel.to_html
    ##########################################

    def test_to_html_001(self):
        html_list = "<div><div>X</div><div>Y</div></div>"
        html_level = "<div>"+html_list+"</div>"

        HTMLGenerator.list_to_html = MagicMock(return_value = html_list)
        HTMLGenerator.wrap = MagicMock(return_value = html_level)

        nodes = Mock()
        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = nodes

        return_value = tree_level.to_html()
        HTMLGenerator.list_to_html.assert_called_once_with(nodes)
        HTMLGenerator.wrap.assert_called_once_with(tree_level, html_list)
        self.assertEqual(return_value, html_level)

if __name__ == '__main__':
    unittest.main()
