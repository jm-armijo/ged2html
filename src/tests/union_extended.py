import unittest
from unittest.mock import MagicMock, Mock, patch, call
from ..union_extended import UnionExtended


class TestUnionExtended(unittest.TestCase):

    ##########################################
    # UnionExtended.__init__
    ##########################################

    @patch("src.union_extended.UnionExtended._extend_nodes")
    @patch("src.union_extended.UnionExtended._arrange_unions")
    def test_init_001(self, mock_arrange_unions, mock_extend_nodes):
        unions = Mock()
        union_extended = UnionExtended(unions)

        self.assertEqual(union_extended.unions, list())
        self.assertEqual(union_extended.nodes, list())

        mock_extend_nodes.assert_called_once_with(unions)
        mock_arrange_unions.assert_called_once()

    ##########################################
    # UnionExtended.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = Mock()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = unions
        actual = union_extended.get_unions()
        self.assertEqual(expected, actual)

    ##########################################
    # UnionExtended.get_spouses
    ##########################################

    def test_get_spouses_001(self):
        unions = list()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = list()
        actual = union_extended.get_spouses()
        self.assertEqual(expected, actual)

    def test_get_spouses_002(self):
        spouse1 = Mock()
        spouse2 = Mock()
        spouses = [spouse1, spouse2]

        union = Mock()
        union.get_spouses = MagicMock(return_value = spouses)
        unions = [union]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = spouses
        actual = union_extended.get_spouses()
        self.assertEqual(expected, actual)

    def test_get_spouses_003(self):
        spouse1 = Mock()
        spouse2 = Mock()
        spouse3 = Mock()
        spouse4 = Mock()
        spouses_1_2 = [spouse1, spouse2]
        spouses_2_3 = [spouse2, spouse3]
        spouses_3_4 = [spouse3, spouse4]

        union1 = Mock()
        union2 = Mock()
        union3 = Mock()
        union1.get_spouses = MagicMock(return_value = spouses_1_2)
        union2.get_spouses = MagicMock(return_value = spouses_2_3)
        union3.get_spouses = MagicMock(return_value = spouses_3_4)
        unions = [union1, union2, union3]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = spouses_1_2 + spouses_2_3 + spouses_3_4
        actual = union_extended.get_spouses()
        self.assertEqual(expected, actual)

    ##########################################
    # UnionExtended.get_parents
    ##########################################

    def test_get_parents_001(self):
        unions = list()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = list()
        actual = union_extended.get_parents()
        self.assertEqual(expected, actual)

    def test_get_parents_002(self):
        parents = list()

        union = Mock()
        union.get_parents = MagicMock(return_value = parents)
        unions = [union]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents
        actual = union_extended.get_parents()
        self.assertEqual(expected, actual)

    def test_get_parents_003(self):
        parent1 = Mock()
        parent2 = Mock()
        parents = [parent1, parent2]

        union = Mock()
        union.get_parents = MagicMock(return_value = parents)
        unions = [union]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents
        actual = union_extended.get_parents()
        self.assertEqual(expected, actual)

    def test_get_parents_004(self):
        parent1 = Mock()
        parent2 = Mock()
        parent3 = Mock()
        parent4 = Mock()
        parents_1_2 = [parent1, parent2]
        parents_3_4 = [parent3, parent4]

        union1 = Mock()
        union2 = Mock()
        union1.get_parents = MagicMock(return_value = parents_1_2)
        union2.get_parents = MagicMock(return_value = parents_3_4)
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = parents_1_2 + parents_3_4
        actual = union_extended.get_parents()
        self.assertEqual(expected, actual)

    ##########################################
    # UnionExtended.get_children
    ##########################################

    def test_get_children_001(self):
        unions = list()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = list()
        actual = union_extended.get_children()
        self.assertEqual(expected, actual)

    def test_get_children_002(self):
        children = list()

        union = Mock()
        union.get_children = MagicMock(return_value = children)
        unions = [union]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = children
        actual = union_extended.get_children()
        self.assertEqual(expected, actual)

    def test_get_children_003(self):
        child1 = Mock()
        child2 = Mock()
        child3 = Mock()
        children = [child1, child2, child3]

        union = Mock()
        union.get_children = MagicMock(return_value = children)
        unions = [union]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = children
        actual = union_extended.get_children()
        self.assertEqual(expected, actual)

    def test_get_children_004(self):
        child1 = Mock()
        child2 = Mock()
        child3 = Mock()
        child4 = Mock()
        children_1_2 = [child1, child2]
        children_3_4 = [child3, child4]

        union1 = Mock()
        union2 = Mock()
        union1.get_children = MagicMock(return_value = children_1_2)
        union2.get_children = MagicMock(return_value = children_3_4)
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = unions

        expected = children_1_2 + children_3_4
        actual = union_extended.get_children()
        self.assertEqual(expected, actual)

    ##########################################
    # UnionExtended.to_html
    ##########################################

    def test_to_html_001(self):
        nodes = list()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes

        expected = ''
        actual = union_extended.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_002(self):
        node1 = Mock()
        node1_html = '<div>node1</div>'
        node1.to_html = MagicMock(return_value = node1_html)
        nodes = [node1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes

        expected = node1_html
        actual = union_extended.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_003(self):
        node1 = Mock()
        node2 = Mock()

        node1_html = '<div>node1</div>'
        node2_html = '<div>node2</div>'

        node1.to_html = MagicMock(return_value = node1_html)
        node2.to_html = MagicMock(return_value = node2_html)

        nodes = [node1, node2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes

        expected = node1_html + node2_html
        actual = union_extended.to_html()
        self.assertEqual(expected, actual)

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

    def test_extend_node_001(self):
        unions = list()
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)
        self.assertEqual(union_extended.unions, list())

    def test_extend_node_002(self):
        union1 = Mock()
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = [union1]

        node = Mock()
        union_extended._extend_node(node)
        self.assertEqual(union_extended.unions, [union1])

    def test_extend_node_003(self):
        union1 = Mock()
        unions = [union1]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)
        self.assertEqual(union_extended.unions, [union1])

    def test_extend_node_004(self):
        union1 = Mock()
        union2 = Mock()
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = [union2]

        node = Mock()
        union_extended._extend_node(node)
        self.assertEqual(union_extended.unions, [union2, union1])

    def test_extend_node_005(self):
        union1 = Mock()
        union2 = Mock()
        unions = [union1, union2]

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._extract_all_unions = MagicMock(return_value = unions)
        union_extended.unions = list()

        node = Mock()
        union_extended._extend_node(node)
        self.assertEqual(union_extended.unions, [union1, union2])

    ##########################################
    # UnionExtended._extract_all_unions
    ##########################################

    @patch("src.unique_queue.UniqueQueue.__new__")
    def test_extract_all_unions_001(self, class_unique_queue):
        unique_queue = Mock()
        unique_queue.is_empty = MagicMock(return_value = True)
        unique_queue.get_all = MagicMock(return_value = list())
        class_unique_queue.return_value = unique_queue

        node = Mock()

        union_extended = UnionExtended.__new__(UnionExtended)

        expected = list()
        actual = union_extended._extract_all_unions(node)
        self.assertEqual(expected, actual)

    @patch("src.unique_queue.UniqueQueue.__new__")
    def test_extract_all_unions_002(self, class_unique_queue):
        all = Mock()
        unions = Mock()

        node = Mock()
        node.get_unions = MagicMock(return_value = unions)

        unique_queue = Mock()
        unique_queue.is_empty = MagicMock(side_effect = [False, True])
        unique_queue.pop = MagicMock(return_value = node)
        unique_queue.push_list = MagicMock()
        unique_queue.get_all = MagicMock(return_value = all)
        class_unique_queue.return_value = unique_queue

        node = Mock()

        union_extended = UnionExtended.__new__(UnionExtended)

        expected = all
        actual = union_extended._extract_all_unions(node)
        self.assertEqual(expected, actual)

        unique_queue.push_list.assert_called_once_with(unions)

    ##########################################
    # UnionExtended._arrange_unions
    ##########################################

    def test_arrange_unions_001(self):
        spouse = Mock()

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._find_spouse_with_one_union = MagicMock(return_value = spouse)
        union_extended._add_spouse = MagicMock()

        union_extended._arrange_unions()
        union_extended._add_spouse.assert_called_once_with(spouse)

    ##########################################
    # UnionExtended._find_spouse_with_one_union
    ##########################################

    def test_find_spouse_with_one_union_001(self):
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = list()

        expected = None
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_002(self):
        union = Mock()
        union.get_spouses = MagicMock(return_value = list())

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union]

        expected = None
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_003(self):
        spouse1 = Mock()
        spouse1.get_unions = MagicMock(return_value = list())
        spouses = [spouse1]

        union = Mock()
        union.get_spouses = MagicMock(return_value = spouses)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union]

        expected = None
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_004(self):
        spouse1_unions = [Mock(), Mock()]
        spouse1 = Mock()
        spouse1.get_unions = MagicMock(return_value = spouse1_unions)
        spouses = [spouse1]

        union = Mock()
        union.get_spouses = MagicMock(return_value = spouses)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union]

        expected = None
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_005(self):
        spouse1_union = Mock()
        spouse1_unions = [spouse1_union]
        spouse1 = Mock()
        spouse1.get_unions = MagicMock(return_value = spouse1_unions)
        spouses = [spouse1]

        union = Mock()
        union.get_spouses = MagicMock(return_value = spouses)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union]

        expected = spouse1
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_006(self):
        spouse2_union = Mock()
        spouse2_unions = [spouse2_union]
        spouse1_unions = [Mock(), Mock()]

        spouse1 = Mock()
        spouse2 = Mock()
        spouse1.get_unions = MagicMock(return_value = spouse1_unions)
        spouse2.get_unions = MagicMock(return_value = spouse2_unions)
        spouses = [spouse1, spouse2]

        union = Mock()
        union.get_spouses = MagicMock(return_value = spouses)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union]

        expected = spouse2
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    def test_find_spouse_with_one_union_007(self):
        unions_spouse1_1 = [Mock(), Mock()]
        unions_spouse1_2 = [Mock(), Mock()]
        unions_spouse2_1 = [Mock(), Mock()]
        unions_spouse2_2 = [Mock()]

        spouse1_1 = Mock()
        spouse1_2 = Mock()
        spouse2_1 = Mock()
        spouse2_2 = Mock()

        spouse1_1.get_unions = MagicMock(return_value = unions_spouse1_1)
        spouse1_2.get_unions = MagicMock(return_value = unions_spouse1_2)
        spouse2_1.get_unions = MagicMock(return_value = unions_spouse2_1)
        spouse2_2.get_unions = MagicMock(return_value = unions_spouse2_2)

        spouses_union1 = [spouse1_1, spouse1_2]
        spouses_union2 = [spouse2_1, spouse2_2]

        union1 = Mock()
        union2 = Mock()
        union1.get_spouses = MagicMock(return_value = spouses_union1)
        union2.get_spouses = MagicMock(return_value = spouses_union2)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.unions = [union1, union2]

        expected = spouse2_2
        actual = union_extended._find_spouse_with_one_union()
        self.assertEqual(actual, expected)

    ##########################################
    # UnionExtended._add_spouse
    ##########################################

    def test_add_spouse_001(self):
        spouse = Mock()

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = list()
        union_extended._add_union_of_spouse = MagicMock()

        expected = [spouse]
        union_extended._add_spouse(spouse)
        actual = union_extended.nodes

        self.assertEqual(expected, actual)
        union_extended._add_union_of_spouse.assert_called_once_with(spouse)

    def test_add_spouse_002(self):
        spouse = Mock()

        nodes = [Mock(), Mock(), Mock()]
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes
        union_extended._add_union_of_spouse = MagicMock()

        expected = nodes + [spouse]
        union_extended._add_spouse(spouse)
        actual = union_extended.nodes

        self.assertEqual(expected, actual)
        union_extended._add_union_of_spouse.assert_called_once_with(spouse)

    def test_add_spouse_003(self):
        spouse = Mock()

        nodes = [Mock(), Mock(), spouse, Mock()]
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes
        union_extended._add_union_of_spouse = MagicMock()

        expected = nodes
        union_extended._add_spouse(spouse)
        actual = union_extended.nodes

        self.assertEqual(expected, actual)
        union_extended._add_union_of_spouse.assert_not_called()

    def test_add_spouse_003(self):
        spouse = Mock()

        nodes = [Mock(), Mock(), spouse]
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes
        union_extended._add_union_of_spouse = MagicMock()

        expected = nodes
        union_extended._add_spouse(spouse)
        actual = union_extended.nodes

        self.assertEqual(expected, actual)
        union_extended._add_union_of_spouse.assert_not_called()

    def test_add_spouse_004(self):
        spouse = Mock()

        nodes = [spouse, Mock()]
        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = nodes
        union_extended._add_union_of_spouse = MagicMock()

        expected = nodes
        union_extended._add_spouse(spouse)
        actual = union_extended.nodes

        self.assertEqual(expected, actual)
        union_extended._add_union_of_spouse.assert_not_called()

    ##########################################
    # UnionExtended._add_union_of_spouse
    ##########################################

    def test_add_union_of_spouse_001(self):
        spouse = Mock()
        union = None

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._find_next_union = MagicMock(return_value = union)
        union_extended._add_spouse = MagicMock()
        union_extended.nodes = list()

        union_extended._add_union_of_spouse(spouse)
        self.assertEqual(union_extended.nodes, list())
        union_extended._add_spouse.assert_not_called()

    def test_add_union_of_spouse_002(self):
        spouse = Mock()
        spouse2 = Mock()
        union = Mock()
        link = Mock()
        union.link = link
        union.get_other_spouse = MagicMock(return_value = spouse2)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended._find_next_union = MagicMock(return_value = union)
        union_extended._add_spouse = MagicMock()
        union_extended.nodes = list()

        union_extended._add_union_of_spouse(spouse)
        self.assertEqual(union_extended.nodes, [link])
        union.get_other_spouse.assert_called_once_with(spouse)
        union_extended._add_spouse.assert_called_once_with(spouse2)

    ##########################################
    # UnionExtended._find_next_union
    ##########################################

    def test_find_next_union_001(self):
        unions = list()
        spouse = Mock()
        spouse.get_unions = MagicMock(return_value=unions)

        union_extended = UnionExtended.__new__(UnionExtended)

        expected = None
        actual = union_extended._find_next_union(spouse)
        self.assertEqual(expected, actual)

    def test_find_next_union_002(self):
        link1 = Mock()

        union1 = Mock()
        union1.link = link1
        unions = [union1]

        spouse = Mock()
        spouse.get_unions = MagicMock(return_value=unions)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = [link1]

        expected = None
        actual = union_extended._find_next_union(spouse)
        self.assertEqual(expected, actual)

    def test_find_next_union_003(self):
        link1 = Mock()

        union1 = Mock()
        union1.link = link1
        unions = [union1]

        spouse = Mock()
        spouse.get_unions = MagicMock(return_value=unions)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = list()

        expected = union1
        actual = union_extended._find_next_union(spouse)
        self.assertEqual(expected, actual)

    def test_find_next_union_004(self):
        link1 = Mock()
        link2 = Mock()

        union1 = Mock()
        union2 = Mock()
        union1.link = link1
        union2.link = link2
        unions = [union1, union2]

        spouse = Mock()
        spouse.get_unions = MagicMock(return_value=unions)

        union_extended = UnionExtended.__new__(UnionExtended)
        union_extended.nodes = [link1]

        expected = union2
        actual = union_extended._find_next_union(spouse)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
