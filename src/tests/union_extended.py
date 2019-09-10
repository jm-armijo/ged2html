import unittest
from unittest.mock import Mock, MagicMock, call, patch
from collections import defaultdict
from ..union_extended import UnionExtended
from ..null_person import NullPerson

class TestUnionExtended(unittest.TestCase):

    ##########################################
    # UnionExtended.__init__
    ##########################################

    @patch("src.union_extended.UnionExtended._extend_nodes")
    def test_init_001(self, mock_extend_nodes):
        unions = [Mock()]
        union_extended = UnionExtended(unions)

        self.assertEqual(union_extended.unions, list())
        mock_extend_nodes.assert_called_once_with(unions)

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
    # UnionExtended.get_spouses
    ##########################################

    def test_get_spouses_001(self):
        union1 = Mock()

        spouse1 = Mock()
        spouse2 = Mock()

        union1.get_spouses = MagicMock(return_value = [spouse1, spouse2])
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = [spouse1, spouse2]
        actual = union_extended.get_spouses()
        self.assertEqual(actual, expected)

    def test_get_spouses_002(self):
        union1 = Mock()
        union2 = Mock()

        spouse1 = Mock()
        spouse2 = Mock()
        spouse3 = Mock()

        union1.get_spouses = MagicMock(return_value = [spouse1, spouse2])
        union2.get_spouses = MagicMock(return_value = [spouse1, spouse3])
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = [spouse1, spouse2, spouse1, spouse3]
        actual = union_extended.get_spouses()
        self.assertEqual(actual, expected)

    ##########################################
    # UnionExtended.get_parents
    ##########################################

    def test_get_parents_001(self):
        union1 = Mock()

        parent1 = Mock()
        parent2 = Mock()
        parents = [parent1, parent2]

        union1.get_parents = MagicMock(return_value = parents)
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents
        actual = union_extended.get_parents()
        self.assertEqual(actual, expected)

    def test_get_parents_002(self):
        union1 = Mock()

        parent1 = Mock()
        parent2 = Mock()
        parent3 = Mock()
        parent4 = Mock()
        parents = [parent1, parent2, parent3, parent4]

        union1.get_parents = MagicMock(return_value = parents)
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents
        actual = union_extended.get_parents()
        self.assertEqual(actual, expected)

    def test_get_parents_003(self):
        union1 = Mock()
        parents = list()

        union1.get_parents = MagicMock(return_value = parents)
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents
        actual = union_extended.get_parents()
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
        html1 = '<div>union1</div>'
        union1 = Mock()

        union1.to_html = MagicMock(return_value = html1)
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = html1
        actual = union_extended.to_html()
        self.assertEqual(actual, expected)

    def test_get_children_002(self):
        html1 = '<div>union1</div>'
        html2 = '<div>union2</div>'

        union1 = Mock()
        union2 = Mock()

        union1.to_html = MagicMock(return_value = html1)
        union2.to_html = MagicMock(return_value = html2)
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = html1 + html2
        actual = union_extended.to_html()
        self.assertEqual(actual, expected)

    def test_get_children_003(self):
        html = ''
        unions = list()

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = html
        actual = union_extended.to_html()
        self.assertEqual(actual, expected)

    ##########################################
    # UnionExtended._extend_nodes
    ##########################################

    def test_extend_nodes_001(self):
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extend_node = MagicMock()

        nodes = list()
        union_extended._extend_nodes(nodes)
        union_extended._extend_node.assert_not_called()

    def test_extend_nodes_002(self):
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extend_node = MagicMock()

        node1 = Mock()
        nodes = [node1]
        union_extended._extend_nodes(nodes)
        union_extended._extend_node.assert_called_once_with(node1)

    def test_extend_nodes_003(self):
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extend_node = MagicMock()

        node1 = Mock()
        node2 = Mock()
        nodes = [node1, node2]
        union_extended._extend_nodes(nodes)
        self.assertEqual(union_extended._extend_node.mock_calls, [call(node1), call(node2)])

    ##########################################
    # UnionExtended._extend_node
    ##########################################

    def test_extend_nodes_001(self):
        union1 = Mock()
        union2 = Mock()
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)

        expected = unions
        self.assertEqual(union_extended.unions, expected)

    def test_extend_nodes_002(self):
        unions = list()

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)

        expected = unions
        self.assertEqual(union_extended.unions, expected)

    def test_extend_nodes_003(self):
        union1 = Mock()
        union2 = Mock()
        union3 = Mock()
        unions = [union1, union2, union1, union3]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)

        expected = [union1, union2, union3]
        self.assertEqual(union_extended.unions, expected)

    ##########################################
    # UnionExtended._extract_all_unions
    ##########################################

    @patch("src.unique_queue.UniqueQueue.__new__")
    def test_extract_all_unions_001(self, class_unique_queue):
        nodes = list()
        queue = Mock()
        queue.is_empty = MagicMock(return_value=True)
        queue.get_all = MagicMock(return_value=nodes)
        class_unique_queue.return_value = queue

        node = Mock()

        union_extended = UnionExtended.__new__(UnionExtended)

        expected = nodes
        actual = union_extended._extract_all_unions(node)
        self.assertEqual(expected, actual)

    @patch("src.unique_queue.UniqueQueue.__new__")
    def test_extract_all_unions_002(self, class_unique_queue):
        nodes = [Mock(), Mock(), Mock()]
        unions = [Mock()]

        queue_node1 = Mock()
        queue_node1.get_unions = MagicMock(return_value=unions)

        queue = Mock()
        queue.is_empty = MagicMock(side_effect=[False, True])
        queue.get_all = MagicMock(return_value=nodes)
        queue.pop = MagicMock(return_value=queue_node1)
        queue.push_list = MagicMock()

        class_unique_queue.return_value = queue

        union_extended = UnionExtended.__new__(UnionExtended)
        input_node = Mock()

        expected = nodes
        actual = union_extended._extract_all_unions(input_node)
        self.assertEqual(expected, actual)

        queue.pop.assert_called_once()
        queue_node1.get_unions.assert_called_once()
        queue.push_list.assert_called_once_with(unions)

if __name__ == '__main__':
    unittest.main()
