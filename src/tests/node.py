import unittest
from ..node import Node

class TestNode(unittest.TestCase):

    ##########################################
    # Node.__init__
    ##########################################

    def test_init_001(self):
        node = Node()
        self.assertEqual(node.children, list())
        self.assertEqual(node.parents, list())

    ##########################################
    # Node.get_children
    ##########################################

    def test_get_children_001(self):
        children = list()
        node = Node.__new__(Node)
        node.children = children

        return_value = node.get_children()
        self.assertEqual(return_value, children)

    ##########################################
    # Node.get_parents
    ##########################################

    def test_get_parents_001(self):
        parents = list()
        node = Node.__new__(Node)
        node.parents = parents

        return_value = node.get_parents()
        self.assertEqual(return_value, parents)

if __name__ == '__main__':
    unittest.main()
