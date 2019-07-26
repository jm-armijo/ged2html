import unittest
from unittest.mock import patch
from ..person import Person

class TestPerson(unittest.TestCase):
	@patch("src.node.Node.__init__")
	def test_init_001(self, mock_init):
		id = "@I1234567@"
		person = Person(id)
		mock_init.assert_called_with(0, 'ID', id)

	@patch("src.node.Node.__init__")
	@patch("src.node.Node.addNode")
	def test_add_attribute_001(self, mock_add, mock_init):
		mock_init.return_value = None

		# Setup Node
		person_obj = Person.__new__(Person)
		person_obj.children = list()

		level = '1'
		attribute = 'ATTR'
		value = 'VAL'
	
		# Actual test
		person_obj.addAttribute(level, attribute, value)
		mock_init.assert_called_with(level, attribute, value)
		self.assertTrue(mock_add.called)

if __name__ == '__main__':
	unittest.main()
