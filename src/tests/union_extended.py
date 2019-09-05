import unittest
from unittest.mock import Mock, MagicMock
from ..union_extended import UnionExtended

class TestUnionExtended(unittest.TestCase):

    ##########################################
    # UnionExtended.__init__
    ##########################################

    def test_init_001(self):
        union_extended = UnionExtended()
        self.assertEqual(union_extended.unions, list())

    ##########################################
    # UnionExtended.add_union
    ##########################################

    def test_add_union_001(self):
        spouse1 = Mock()
        spouse2 = Mock()
        union = Mock()
        union.get_spouse1 = MagicMock(return_value = spouse1)
        union.get_spouse2 = MagicMock(return_value = spouse2)

        expected_unions = [union]
        expected_nodes = [spouse1, spouse2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = list()
        union_extended.nodes = list()

        union_extended.add_union(union)
        self.assertEqual(union_extended.unions, expected_unions)
        self.assertEqual(union_extended.nodes, expected_nodes)
        
    def test_add_union_002(self):
        spouse1 = Mock()
        spouse2 = Mock()
        spouse3 = Mock()

        union1 = Mock()
        union2 = Mock()
        union2.get_spouse1 = MagicMock(return_value = spouse3)
        union2.get_spouse2 = MagicMock(return_value = spouse2)

        expected_unions = [union1, union2]
        expected_nodes = [spouse1, spouse2, spouse3]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union1]
        union_extended.nodes = [spouse1, spouse2]

        union_extended.add_union(union2)
        self.assertEqual(union_extended.unions, expected_unions)
        self.assertEqual(union_extended.nodes, expected_nodes)

    def test_add_union_003(self):
        spouse1 = Mock()
        spouse2 = Mock()
        spouse3 = Mock()

        union1 = Mock()
        union2 = Mock()
        union2.get_spouse1 = MagicMock(return_value = spouse1)
        union2.get_spouse2 = MagicMock(return_value = spouse3)

        expected_unions = [union1, union2]
        expected_nodes = [spouse3, spouse1, spouse2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union1]
        union_extended.nodes = [spouse1, spouse2]

        union_extended.add_union(union2)
        self.assertEqual(union_extended.unions, expected_unions)
        self.assertEqual(union_extended.nodes, expected_nodes)
        
    ##########################################
    # UnionExtended.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = [Mock(), Mock()]
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = unions
        actual = union_extended.get_unions()
        self.assertEqual(actual, expected)

    def test_get_unions_002(self):
        unions = []
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = unions
        actual = union_extended.get_unions()
        self.assertEqual(actual, expected)

    ##########################################
    # UnionExtended.get_children
    ##########################################

    def test_get_children_001(self):
        union1 = Mock()
        union2 = Mock()

        union1.get_children = MagicMock(return_value = [])
        union2.get_children = MagicMock(return_value = [])

        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = []
        actual = union_extended.get_children()
        self.assertEqual(actual, expected)

    def test_get_children_002(self):
        child_1_1 = Mock()
        child_1_2 = Mock()
        child_2_1 = Mock()
        child_2_2 = Mock()

        union1 = Mock()
        union2 = Mock()

        union1.get_children = MagicMock(return_value = [child_1_1, child_1_2])
        union2.get_children = MagicMock(return_value = [child_2_1, child_2_2])

        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = [child_1_1, child_1_2, child_2_1, child_2_2]
        actual = union_extended.get_children()
        self.assertEqual(actual, expected)

    ##########################################
    # UnionExtended.to_html
    ##########################################

    def test_get_children_001(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
