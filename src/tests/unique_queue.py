import unittest
from unittest.mock import MagicMock, Mock, call
from ..unique_queue import unique_queue
from collections import deque

class TestPerson(unittest.TestCase):

	##########################################
	# unique_queue.__init__
	##########################################

	def test_init_001(self):
		queue = unique_queue()
		self.assertEqual(queue.opened, list())
		self.assertEqual(queue.to_open, deque())

	def test_init_002(self):
		unions = []
		queue = unique_queue(unions)
		self.assertEqual(queue.opened, list())
		self.assertEqual(queue.to_open, deque())

	def test_init_002(self):
		union = Mock()
		unions = [union]
		queue = unique_queue(unions)
		self.assertEqual(queue.opened, list())
		self.assertEqual(queue.to_open, deque([union]))

	##########################################
	# unique_queue.pushList
	##########################################

	def test_push_list_001(self):
		element1 = Mock()
		element2 = Mock()
		elements = [element1, element2]

		queue = unique_queue.__new__(unique_queue)
		queue.push = MagicMock()

		queue.pushList(elements)
		self.assertEqual(queue.push.mock_calls, [call(element1), call(element2)])

	def test_push_list_001(self):
		elements = []

		queue = unique_queue.__new__(unique_queue)
		queue.push = MagicMock()

		queue.pushList(elements)
		queue.push.assert_not_called()

	##########################################
	# unique_queue.push
	##########################################

	def test_push_001(self):
		element = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = list()
		queue.to_open = deque()

		queue.push(element)
		self.assertTrue(element in queue.to_open)
		self.assertFalse(element in queue.opened)

	def test_push_002(self):
		element = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = [element]
		queue.to_open = deque()

		queue.push(element)
		self.assertFalse(element in queue.to_open)
		self.assertTrue(element in queue.opened)

	def test_push_003(self):
		element = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = []
		queue.to_open = deque([element])

		queue.push(element)
		self.assertEqual(len(queue.to_open), 1)
		self.assertTrue(element in queue.to_open)
		self.assertFalse(element in queue.opened)

	##########################################
	# unique_queue.pop
	##########################################

	def test_pop_001(self):
		queue = unique_queue.__new__(unique_queue)
		queue.opened = list()
		queue.to_open = deque()

		element = queue.pop()
		self.assertEqual(element, None)

	def test_pop_002(self):
		queue = unique_queue.__new__(unique_queue)
		queue.opened = [Mock()]
		queue.to_open = deque()

		element = queue.pop()
		self.assertEqual(element, None)

	def test_pop_003(self):
		element = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = [Mock()]
		queue.to_open = deque([element])

		returned_element = queue.pop()
		self.assertEqual(returned_element, element)
		self.assertFalse(element in queue.to_open)
		self.assertTrue(element in queue.opened)

	def test_pop_004(self):
		element = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = [Mock()]
		queue.to_open = deque([element, Mock(), Mock()])

		returned_element = queue.pop()
		self.assertEqual(returned_element, element)
		self.assertFalse(element in queue.to_open)
		self.assertTrue(element in queue.opened)

	##########################################
	# unique_queue.isEmpty
	##########################################

	def test_is_empty_001(self):
		queue = unique_queue.__new__(unique_queue)
		queue.to_open = deque()
		self.assertTrue(queue.isEmpty())

	def test_is_empty_002(self):
		queue = unique_queue.__new__(unique_queue)
		queue.to_open = deque([Mock()])
		self.assertFalse(queue.isEmpty())

	##########################################
	# unique_queue.getAll
	##########################################

	def test_get_all_001(self):
		opened = Mock()
		queue = unique_queue.__new__(unique_queue)
		queue.opened = opened
		self.assertEqual(queue.getAll(), opened)

if __name__ == '__main__':
	unittest.main()
