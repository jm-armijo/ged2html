import unittest
from ..union import Union


class TestUnion(unittest.TestCase):

	def test_init_001(self):
		id = "@F1234567@"
		node = Union(id)

		self.assertEqual(node.id, id)
		self.assertEqual(node.spouse1, None)
		self.assertEqual(node.spouse2, None)
		self.assertEqual(node.children, list())
		self.assertEqual(node.date, None)
		self.assertEqual(node.place, None)

	def test_set_spouse1(self):
		node = Union.__new__(Union)
		spouse = 'Husband id'
		node.setSpouse1(spouse)
		self.assertEqual(node.spouse1, spouse)

	def test_set_spouse2(self):
		node = Union.__new__(Union)
		spouse = 'Wife id'
		node.setSpouse2(spouse)
		self.assertEqual(node.spouse2, spouse)

	def test_add_child_001(self):
		node = Union.__new__(Union)
		node.children = list()

		child = 'Child 1'
		node.addChild(child)
		self.assertEqual(node.children, [child])

	def test_add_child_002(self):
		node = Union.__new__(Union)
		child1 = 'Child 1'
		child2 = 'Child 2'
		child3 = 'Child 3'
		node.children = [child1, child2]

		node.addChild(child3)
		self.assertEqual(node.children, [child1, child2, child3])

	def test_set_date(self):
		node = Union.__new__(Union)
		date = '28 FEB 1800'
		node.setDate(date)
		self.assertEqual(node.date, date)

	def test_set_place(self):
		node = Union.__new__(Union)
		place = 'Somewhere'
		node.setPlace(place)
		self.assertEqual(node.place, place)

