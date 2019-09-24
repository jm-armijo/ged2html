import unittest
from unittest.mock import MagicMock, Mock, patch
from ..html import HTMLGenerator
from ..person import Person
from ..union import Union


class TestUnion(unittest.TestCase):

    ##########################################
    # Union.__init__
    ##########################################

    @patch("src.person.Person.__new__")
    @patch("src.union_link.UnionLink.__new__")
    def test_init_001(self, class_union_link, class_null_person):
        id = "@F1234567@"
        person1 = Mock()
        person2 = Mock()
        class_null_person.side_effect = [person1, person2]

        union_link = Mock()
        class_union_link.return_value = union_link

        union = Union(id)
        self.assertEqual(union.id, id)
        self.assertEqual(union.spouse1, person1)
        self.assertEqual(union.spouse2, person2)
        self.assertEqual(union.children, list())
        self.assertEqual(union.link, union_link)

    ##########################################
    # Union.set_spouse1
    ##########################################

    def test_set_spouse1(self):
        spouse = Mock()
        spouse.add_union = MagicMock()

        union = Union.__new__(Union)
        union.set_spouse1(spouse)
        self.assertEqual(union.spouse1, spouse)
        spouse.add_union.assert_called_with(union)

    ##########################################
    # Union.set_spouse2
    ##########################################

    def test_set_spouse2(self):
        spouse = Mock()
        spouse.add_union = MagicMock()

        union = Union.__new__(Union)
        union.set_spouse2(spouse)
        self.assertEqual(union.spouse2, spouse)
        spouse.add_union.assert_called_with(union)

    ##########################################
    # Union.add_child
    ##########################################

    def test_add_child_001(self):
        child = Mock()
        child.set_parents = MagicMock()

        union = Union.__new__(Union)
        union.children = list()
        union.add_child(child)
        self.assertEqual(union.children, [child])
        child.set_parents.assert_called_with(union)

    def test_add_child_002(self):
        child1 = Mock()
        child2 = Mock()
        child3 = Mock()
        child3.set_parents = MagicMock()

        union = Union.__new__(Union)
        union.children = [child1, child2]
        union.add_child(child3)
        self.assertEqual(union.children, [child1, child2, child3])
        child3.set_parents.assert_called_with(union)

    ##########################################
    # Union.set_date
    ##########################################

    def test_set_date_001(self):
        union = Union.__new__(Union)
        union.link = Mock()

        date = '28 FEB 1800'
        union.set_date(date)
        self.assertEqual(union.link.date, date)

    ##########################################
    # Union.set_place
    ##########################################

    def test_set_place_001(self):
        union = Union.__new__(Union)
        union.link = Mock()

        place = 'Somewhere'
        union.set_place(place)
        self.assertEqual(union.link.place, place)

    ##########################################
    # Union.get_spouses
    ##########################################

    def test_get_spouses_001(self):
        spouse1 = Mock()
        spouse2 = Mock()

        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        expected = [spouse1, spouse2]
        actual = union.get_spouses()
        self.assertEqual(expected, expected)

    ##########################################
    # Union.get_other_spouse
    ##########################################

    def test_get_other_spouse_001(self):
        spouse1 = Mock()
        spouse2 = Mock()

        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        expected = spouse2
        actual = union.get_other_spouse(spouse1)
        self.assertEqual(expected, actual)

    def test_get_other_spouse_002(self):
        spouse1 = Mock()
        spouse2 = Mock()

        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        expected = spouse1
        actual = union.get_other_spouse(spouse2)
        self.assertEqual(expected, actual)

    ##########################################
    # Union.get_children
    ##########################################

    def test_get_children_001(self):
        children = Mock()
        union = Union.__new__(Union)
        union.children = children

        returned_children = union.get_children()
        self.assertEqual(returned_children, children)

    def test_get_children_002(self):
        union = Union.__new__(Union)
        union.spouse1 = None
        union.spouse2 = None

        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, [])

    def test_get_children_003(self):
        # Setup parents
        parents1 = [Mock()]
        parents2 = []

        # Setup spouses
        spouse1 = Mock()
        spouse1.get_parents = MagicMock(return_value = parents1)

        spouse2 = Mock()
        spouse2.get_parents = MagicMock(return_value = parents2)

        # Setup union of spouses
        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        # Test
        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents1)

    def test_get_children_003(self):
        # Setup parents
        parents1 = []
        parents2 = [Mock()]

        # Setup spouses
        spouse1 = Mock()
        spouse1.get_parents = MagicMock(return_value = parents1)

        spouse2 = Mock()
        spouse2.get_parents = MagicMock(return_value = parents2)

        # Setup union of spouses
        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        # Test
        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents2)

    def test_get_children_004(self):
        # Setup parents
        parents1 = [Mock()]
        parents2 = [Mock()]

        # Setup spouses
        spouse1 = Mock()
        spouse1.get_parents = MagicMock(return_value = parents1)

        spouse2 = Mock()
        spouse2.get_parents = MagicMock(return_value = parents2)

        # Setup union of spouses
        union = Union.__new__(Union)
        union.spouse1 = spouse1
        union.spouse2 = spouse2

        # Test
        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents1 + parents2)

    ##########################################
    # Union.get_parents
    ##########################################

    def test_get_parents_001(self):
        parents = list()
        union = Union.__new__(Union)
        union.spouse1 = None
        union.spouse2 = None

        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents)

    def test_get_parents_002(self):
        parents_spouse2 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = None
        union.spouse2 = Mock()
        union.spouse2.get_parents = MagicMock(return_value = parents_spouse2)

        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents_spouse2)

    def test_get_parents_003(self):
        parents_spouse1 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = Mock()
        union.spouse1.get_parents = MagicMock(return_value = parents_spouse1)
        union.spouse2 = None

        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents_spouse1)

    def test_get_parents_004(self):
        parents_spouse1 = [Mock()]
        parents_spouse2 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = Mock()
        union.spouse1.get_parents = MagicMock(return_value = parents_spouse1)
        union.spouse2 = Mock()
        union.spouse2.get_parents = MagicMock(return_value = parents_spouse2)

        returned_parents = union.get_parents()
        self.assertEqual(returned_parents, parents_spouse1 + parents_spouse2)

    ##########################################
    # Union.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = list()
        union = Union.__new__(Union)
        union.spouse1 = None
        union.spouse2 = None

        returned_unions = union.get_unions()
        self.assertEqual(returned_unions, unions)

    def test_get_unions_002(self):
        unions_spouse2 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = None
        union.spouse2 = Mock()
        union.spouse2.get_unions = MagicMock(return_value = unions_spouse2)

        returned_unions = union.get_unions()
        self.assertEqual(returned_unions, unions_spouse2)

    def test_get_unions_003(self):
        unions_spouse1 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = Mock()
        union.spouse1.get_unions = MagicMock(return_value = unions_spouse1)
        union.spouse2 = None

        returned_unions = union.get_unions()
        self.assertEqual(returned_unions, unions_spouse1)

    def test_get_unions_004(self):
        unions_spouse1 = [Mock()]
        unions_spouse2 = [Mock()]

        union = Union.__new__(Union)
        union.spouse1 = Mock()
        union.spouse1.get_unions = MagicMock(return_value = unions_spouse1)
        union.spouse2 = Mock()
        union.spouse2.get_unions = MagicMock(return_value = unions_spouse2)

        returned_unions = union.get_unions()
        self.assertEqual(returned_unions, unions_spouse1 + unions_spouse2)

    ##########################################
    # Union.to_html()
    ##########################################

    def test_to_html_001(self):
        union = Union.__new__(Union)
        union.id = '@F00003@'
        union.date = '20-02-2002'
        union.spouse1 = Mock()
        union.spouse2 = Mock()
        union.link = Mock()

        spouse1_html = "<div>Spouse1</div>"
        spouse2_html = "<div>Spouse2</div>"
        link_html = "<div>link</div>"

        union.spouse1.to_html = MagicMock(return_value = spouse1_html)
        union.spouse2.to_html = MagicMock(return_value = spouse2_html)
        union.link.to_html = MagicMock(return_value = link_html)

        value = (
            '  {}\n'
            '  {}\n'
            '  {}\n'
        ).format(spouse1_html, link_html, spouse2_html)

        wrapped = "<div>"+value+"</div>"
        HTMLGenerator.wrap_instance = MagicMock(return_value = wrapped)

        html = union.to_html()
        HTMLGenerator.wrap_instance.assert_called_once_with(union, value)
        self.assertEqual(wrapped, html)

    def test_to_html_002(self):
        union = Union.__new__(Union)
        union.id = '@F00003@'
        union.date = ''
        union.spouse1 = Mock()
        union.spouse2 = Mock()
        union.link = Mock()

        spouse1_html = "<div>Spouse1</div>"
        spouse2_html = ""
        link_html = "<div>link</div>"

        union.spouse1.to_html = MagicMock(return_value = spouse1_html)
        union.spouse2.to_html = MagicMock(return_value = spouse2_html)
        union.link.to_html = MagicMock(return_value = link_html)

        value = (
            '  {}\n'
            '  {}\n'
            '  {}\n'
        ).format(spouse1_html, link_html, spouse2_html)

        wrapped = "<div>"+value+"</div>"
        HTMLGenerator.wrap_instance = MagicMock(return_value = wrapped)

        html = union.to_html()
        HTMLGenerator.wrap_instance.assert_called_once_with(union, value)
        self.assertEqual(wrapped, html)

    ##########################################
    # Union.__str__
    ##########################################

    def test_str_001(self):
        union = Union.__new__(Union)
        union.id = "@F1234567@"
        union.children = list()
        union.date = None
        union.place = None

        union.spouse1 = Mock()
        union.spouse2 = Mock()
        union.spouse1.__str__ = MagicMock(return_value = '[Name Spouse 1]')
        union.spouse2.__str__ = MagicMock(return_value = '[Name Spouse 2]')

        self.assertEqual(str(union), "{ [Name Spouse 1] & [Name Spouse 2] }")

    def test_str_002(self):
        union = Union.__new__(Union)
        union.id = "@F1234567@"
        union.children = list()
        union.date = None
        union.place = None
        union.spouse1 = None

        union.spouse2 = Mock()
        union.spouse2.__str__ = MagicMock(return_value = '[Name Spouse 2]')

        self.assertEqual(str(union), "{ None & [Name Spouse 2] }")

if __name__ == '__main__':
    unittest.main()
