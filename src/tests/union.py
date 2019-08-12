import unittest
from unittest.mock import MagicMock, Mock
from ..union import Union


class TestUnion(unittest.TestCase):

	def test_init_001(self):
		id = "@F1234567@"
		union = Union(id)

		self.assertEqual(union.id, id)
		self.assertEqual(union.spouse1, None)
		self.assertEqual(union.spouse2, None)
		self.assertEqual(union.children, list())
		self.assertEqual(union.date, None)
		self.assertEqual(union.place, None)

	def test_set_spouse1(self):
		spouse = Mock()
		spouse.addUnion = MagicMock()

		union = Union.__new__(Union)
		union.setSpouse1(spouse)
		self.assertEqual(union.spouse1, spouse)
		spouse.addUnion.assert_called_with(union)

	def test_set_spouse2(self):
		spouse = Mock()
		spouse.addUnion = MagicMock()

		union = Union.__new__(Union)
		union.setSpouse2(spouse)
		self.assertEqual(union.spouse2, spouse)
		spouse.addUnion.assert_called_with(union)

	def test_add_child_001(self):
		child = Mock()
		child.setParents = MagicMock()

		union = Union.__new__(Union)
		union.children = list()
		union.addChild(child)
		self.assertEqual(union.children, [child])
		child.setParents.assert_called_with(union)

	def test_add_child_002(self):
		child1 = Mock()
		child2 = Mock()
		child3 = Mock()
		child3.setParents = MagicMock()

		union = Union.__new__(Union)
		union.children = [child1, child2]
		union.addChild(child3)
		self.assertEqual(union.children, [child1, child2, child3])
		child3.setParents.assert_called_with(union)

	def test_set_date(self):
		union = Union.__new__(Union)
		date = '28 FEB 1800'
		union.setDate(date)
		self.assertEqual(union.date, date)

	def test_set_place(self):
		union = Union.__new__(Union)
		place = 'Somewhere'
		union.setPlace(place)
		self.assertEqual(union.place, place)

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
