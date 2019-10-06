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

    def test_append_001(self):
        tree_node = Mock()

        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = list()

        tree_level.append(tree_node)
        self.assertEqual(tree_level.nodes, [tree_node])

    def test_append_002(self):
        node = Mock()
        tree_node1 = Mock()
        tree_node2 = Mock()

        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = [tree_node1]

        tree_level.append(tree_node2)
        self.assertEqual(tree_level.nodes, [tree_node1, tree_node2])

    ##########################################
    # TreeLevel.to_html
    ##########################################

    def test_to_html_001(self):
        html_list = "<div><div>X</div><div>Y</div></div>"
        html_level = "<div>"+html_list+"</div>"

        HTMLGenerator.list_to_html = MagicMock(return_value = html_list)
        HTMLGenerator.wrap_instance = MagicMock(return_value = html_level)

        nodes = Mock()
        tree_level = TreeLevel.__new__(TreeLevel)
        tree_level.nodes = nodes

        return_value = tree_level.to_html()
        HTMLGenerator.list_to_html.assert_called_once_with(nodes)
        HTMLGenerator.wrap_instance.assert_called_once_with(tree_level, html_list)
        self.assertEqual(return_value, html_level)

if __name__ == '__main__':
    unittest.main()
