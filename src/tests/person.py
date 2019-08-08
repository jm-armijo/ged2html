import unittest
from unittest.mock import call, Mock, patch
from ..person import Person

class TestPerson(unittest.TestCase):
	@patch("src.node.Node.__init__")
	def test_init_001(self, mock_init):
		id = "@I1234567@"
		person = Person(id)
		mock_init.assert_called_with(0, 'ID', id)

	'''
	Validate function to add node is called for any attribute key not NAME
	'''
	@patch("src.node.Node.__init__")
	@patch("src.node.Node.addNode")
	def test_add_attribute_001(self, mock_add, mock_init):
		mock_init.return_value = None

		# Setup Node
		person_obj = Person.__new__(Person)
		person_obj.children = list()

		level = '1'
		key = 'ATTR'
		value = 'VAL'

		# Actual test
		person_obj.addAttribute(level, key, value)
		mock_init.assert_called_with(level, key, value)
		self.assertTrue(mock_add.called)

	'''
	Validate function to add a person's name is called for attribute key NAME
	'''
	@patch("src.person.Person.addName")
	def test_add_attribute_001(self, mock_add):
		# Setup Node
		person_obj = Person.__new__(Person)
		person_obj.children = list()

		level = '1'
		key = 'NAME'
		value = 'VAL'

		# Actual test
		person_obj.addAttribute(level, key, value)
		mock_add.assert_called_with(level, key, value)

	##########################################
	# Person.addPersonName
	##########################################

	@patch.object(Person, 'splitName')
	@patch("src.node.Node.addNode")
	def test_add_person_name_001(self, mock_add, mock_split):
		# Mock split function
		first_name = 'First Name'
		last_name = 'Last Name'
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup attribute
		level = 1
		key = 'NAME'
		value = "{} /{}/".format(first_name, last_name)

		# Setup person
		person_obj = Person.__new__(Person)
		person_obj.addName(level, key, value)

		# Actual test
		calls = [
			call(1, 'NAME', ""),
			call(2, 'GIVN', first_name),
			call(2, 'LAST', last_name)
		]
		mock_add.assert_has_calls(calls)
		self.assertEqual(mock_add.call_count, len(calls))

	@patch.object(Person, 'splitName')
	@patch("src.node.Node.addNode")
	def test_add_person_name_002(self, mock_add, mock_split):
		# Mock split function
		first_name = ''
		last_name = 'Last Name'
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup attribute
		level = 1
		key = 'NAME'
		value = "{} /{}/".format(first_name, last_name)

		# Setup person
		person_obj = Person.__new__(Person)
		person_obj.addName(level, key, value)

		# Actual test
		calls = [
			call(1, 'NAME', ""),
			call(2, 'GIVN', first_name),
			call(2, 'LAST', last_name)
		]
		mock_add.assert_has_calls(calls)
		self.assertEqual(mock_add.call_count, len(calls))

	@patch.object(Person, 'splitName')
	@patch("src.node.Node.addNode")
	def test_add_person_name_003(self, mock_add, mock_split):
		# Mock split function
		first_name = 'First Name'
		last_name = ''
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup attribute
		level = 1
		key = 'NAME'
		value = "{} /{}/".format(first_name, last_name)

		# Setup person
		person_obj = Person.__new__(Person)
		person_obj.addName(level, key, value)

		# Actual test
		calls = [
			call(1, 'NAME', ""),
			call(2, 'GIVN', first_name),
			call(2, 'LAST', last_name)
		]
		mock_add.assert_has_calls(calls)
		self.assertEqual(mock_add.call_count, len(calls))

	##########################################
	# Person.splitName
	##########################################

	def test_split_name_001(self):
		parser_obj = Person.__new__(Person)
		full_name = 'First Name /Last Name/'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_002(self):
		parser_obj = Person.__new__(Person)
		full_name = '     First Name    /    Last Name   /   '

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_003(self):
		parser_obj = Person.__new__(Person)
		full_name = '/Last Name/'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('', 'Last Name'))

	def test_split_name_004(self):
		parser_obj = Person.__new__(Person)
		full_name = 'First Name //'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', ''))

	def test_split_name_005(self):
		parser_obj = Person.__new__(Person)
		full_name = 'First Name /Last Name'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

if __name__ == '__main__':
	unittest.main()
