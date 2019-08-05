import unittest
from unittest.mock import patch
from unittest.mock import Mock
from ..parser import Parser

class TestParser(unittest.TestCase):

	##########################################
	# Parser.init
	##########################################

	def test_init_001(self):
		parser = Parser()
		self.assertEqual(len(parser.people),0)
		self.assertIsNone(parser.current_line)
		self.assertEqual(parser.state, 'IDLE')

	##########################################
	# Parser.parse_lines
	##########################################

	@patch.object(Parser, 'getCurrentState')
	@patch.object(Parser, 'parseCurrentLine')
	def test_parse_lines_001(self, mock_parse, mock_get):
		# Setup
		lines = [Mock(), Mock(), Mock()]
		parser_obj = Parser.__new__(Parser)
		parser_obj.people = dict()

		# Actual test
		people = parser_obj.parseLines(lines)
		self.assertEqual(mock_get.call_count, len(lines))
		self.assertEqual(mock_parse.call_count, len(lines))
		self.assertEqual(people, parser_obj.people)

	##########################################
	# Parser.get_current_state
	##########################################

	# From any state goes to INDI when level = 0
	def test_get_current_state_001(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI')

	# From any state goes to FAM when level = 0
	def test_get_current_state_002(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'FAM'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM')

	# Stays on IDLE if level > 0
	def test_get_current_state_003(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'IDLE'
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From FAM goes to IDLE if no more data
	def test_get_current_state_004(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'FAM'
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to IDLE if no more data
	def test_get_current_state_005(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'INDI'
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to INDI_DATA (level 1)
	def test_get_current_state_006(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI goes to INDI_DATA (level 9999)
	def test_get_current_state_007(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 1)
	def test_get_current_state_008(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 9999)
	def test_get_current_state_009(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From FAM goes to FAM_DATA (level 1)
	def test_get_current_state_010(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM goes to FAM_DATA (level 9999)
	def test_get_current_state_011(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 1)
	def test_get_current_state_012(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 9999)
	def test_get_current_state_013(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	##########################################
	# Parser.get_current_line
	##########################################

	@patch.object(Parser, 'createPerson')
	@patch.object(Parser, 'addPersonData')
	def test_parse_current_line_001(self, mock_add, mock_new):
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI'
		parser_obj.parseCurrentLine()
		self.assertTrue(mock_new.called)
		self.assertFalse(mock_add.called)

	@patch.object(Parser, 'createPerson')
	@patch.object(Parser, 'addPersonData')
	def test_parse_current_line_002(self, mock_add, mock_new):
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI_DATA'
		parser_obj.parseCurrentLine()
		self.assertFalse(mock_new.called)
		self.assertTrue(mock_add.called)

	@patch.object(Parser, 'createPerson')
	@patch.object(Parser, 'addPersonData')
	def test_parse_current_line_003(self, mock_add, mock_new):
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM'
		parser_obj.parseCurrentLine()
		self.assertFalse(mock_new.called)
		self.assertFalse(mock_add.called)

	@patch.object(Parser, 'createPerson')
	@patch.object(Parser, 'addPersonData')
	def test_parse_current_line_004(self, mock_add, mock_new):
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM_DATA'
		parser_obj.parseCurrentLine()
		self.assertFalse(mock_new.called)
		self.assertFalse(mock_add.called)

	@patch.object(Parser, 'createPerson')
	@patch.object(Parser, 'addPersonData')
	def test_parse_current_line_005(self, mock_add, mock_new):
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'IDLE'
		parser_obj.parseCurrentLine()
		self.assertFalse(mock_new.called)
		self.assertFalse(mock_add.called)

	##########################################
	# Parser.createPerson
	##########################################

	@patch("src.person.Person.__new__")
	def test_create_person_001(self, mock):
		# Setup person
		person_id = '@I000123@'
		person = Mock()
		person.value = person_id

		# Mock person
		mock.return_value = person

		# Setup line
		line = Mock()
		line.attribute = person_id

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = line
		parser_obj.last_person = person_id
		parser_obj.people = dict()

		# Actual test
		parser_obj.createPerson()
		self.assertEqual(len(parser_obj.people), 1)
		self.assertEqual(parser_obj.people[person.value], person)

	'''
	When creating 3 Person objects with different values, all of them are crated
	'''
	@patch("src.person.Person.__new__")
	def test_create_person_002(self, mock):
		# Setup people
		person1_id = '@I000123@'
		person2_id = '@I000223@'
		person3_id = '@I000323@'

		person1 = Mock()
		person2 = Mock()
		person3 = Mock()

		person1.value = person1_id
		person2.value = person2_id
		person3.value = person3_id

		# Mock person
		mock.side_effect = [person1, person2, person3]

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = None
		parser_obj.people = dict()

		# Create Person 1
		line = Mock()
		line.attribute = person1_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Create Person 2
		line = Mock()
		line.attribute = person2_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Create Person 3
		line = Mock()
		line.attribute = person3_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Actual test
		self.assertEqual(len(parser_obj.people), 3)
		self.assertEqual(parser_obj.people[person3.value], person3)
		self.assertEqual(parser_obj.people[person2.value], person2)
		self.assertEqual(parser_obj.people[person1.value], person1)

	'''
	When creating Person objects with duplicated values, the duplicated replaces the original
	'''
	@patch("src.person.Person.__new__")
	def test_create_person_002(self, mock):
		# Setup people
		dup_id = '@I000123@'
		person3_id = '@I000323@'

		person1 = Mock()
		person2 = Mock()
		person3 = Mock()

		person1.value = dup_id
		person2.value = dup_id
		person3.value = person3_id

		# Mock person
		mock.side_effect = [person1, person2, person3]

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = None
		parser_obj.people = dict()

		# Create Person 1
		line = Mock()
		line.attribute = dup_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Create Person 2
		line = Mock()
		line.attribute = dup_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Create Person 3
		line = Mock()
		line.attribute = person3_id
		parser_obj.current_line = line
		parser_obj.createPerson()

		# Actual test
		self.assertEqual(len(parser_obj.people), 2)
		self.assertEqual(parser_obj.people[person3.value], person3)
		self.assertEqual(parser_obj.people[dup_id], person2)

	##########################################
	# Parser.addPersonData
	##########################################

	@patch.object(Parser, 'addPersonName')
	def test_add_person_data_001(self, mock):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()
		parser_obj.current_line.attribute = 'NAME'
		parser_obj.people = dict()

		# Actual test
		parser_obj.addPersonName()
		self.assertTrue(mock.called)

	@patch.object(Parser, 'addPersonAttribute')
	def test_add_person_data_002(self, mock):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()
		parser_obj.current_line.attribute = 'NO NAME'
		parser_obj.people = dict()

		# Actual test
		parser_obj.addPersonAttribute()
		self.assertTrue(mock.called)

	##########################################
	# Parser.addPersonName
	##########################################

	@patch.object(Parser, 'splitName')
	def test_add_person_name_001(self, mock_split):
		# Mock split function
		first_name = 'First Name'
		last_name = 'Last Name'
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup line
		line = Mock()
		line.data = "{} /{}/".format(first_name, last_name)

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = '@I0001234@'
		parser_obj.people = {'@I0001234@': mock_person}
		parser_obj.current_line = line

		# Actual test
		parser_obj.addPersonName()
		self.assertTrue(mock_person.addAttribute.called_with(1, 'NAME', ""))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'GIVN', first_name))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'LAST', last_name))

	@patch.object(Parser, 'splitName')
	def test_add_person_name_002(self, mock_split):
		# Mock split function
		first_name = ''
		last_name = 'Last Name'
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup line
		line = Mock()
		line.data = "{} /{}/".format(first_name, last_name)

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = '@I0001234@'
		parser_obj.people = {'@I0001234@': mock_person}
		parser_obj.current_line = line

		# Actual test
		parser_obj.addPersonName()
		self.assertTrue(mock_person.addAttribute.called_with(1, 'NAME', ""))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'GIVN', first_name))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'LAST', last_name))

	@patch.object(Parser, 'splitName')
	def test_add_person_name_003(self, mock_split):
		# Mock split function
		first_name = 'First Name'
		last_name = ''
		mock_split.return_value = (first_name, last_name)

		# Mock person
		mock_person = Mock()

		# Setup line
		line = Mock()
		line.data = "{} /{}/".format(first_name, last_name)

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = '@I0001234@'
		parser_obj.people = {'@I0001234@': mock_person}
		parser_obj.current_line = line

		# Actual test
		parser_obj.addPersonName()
		self.assertTrue(mock_person.addAttribute.called_with(1, 'NAME', ""))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'GIVN', first_name))
		self.assertTrue(mock_person.addAttribute.called_with(2, 'LAST', last_name))

	##########################################
	# Parser.addPersonAttribute
	##########################################

	def test_add_person_attribute_001(self):
		# Setup line
		attribute = 'KEY'
		level = 2
		data = "Some data"

		line = Mock()
		line.level = level
		line.data = data

		# Mock person
		mock_person = Mock()

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = '@I0001234@'
		parser_obj.people = {'@I0001234@': mock_person}
		parser_obj.current_line = line

		# Actual test
		parser_obj.addPersonAttribute(attribute)
		self.assertTrue(mock_person.addAttribute.called_with(level, attribute, data))

	def test_add_person_attribute_002(self):
		# Setup line
		attribute = 'KEY'
		level = 2
		data = ''

		line = Mock()
		line.level = level
		line.data = data

		# Mock person
		mock_person = Mock()

		# Setup parser
		parser_obj = Parser.__new__(Parser)
		parser_obj.last_person = '@I0001234@'
		parser_obj.people = {'@I0001234@': mock_person}
		parser_obj.current_line = line

		# Actual test
		parser_obj.addPersonAttribute(attribute)
		self.assertTrue(mock_person.addAttribute.called_with(level, attribute, data))

	##########################################
	# Parser.splitName
	##########################################

	def test_split_name_001(self):
		parser_obj = Parser.__new__(Parser)
		full_name = 'First Name /Last Name/'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_002(self):
		parser_obj = Parser.__new__(Parser)
		full_name = '     First Name    /    Last Name   /   '

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_003(self):
		parser_obj = Parser.__new__(Parser)
		full_name = '/Last Name/'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('', 'Last Name'))

	def test_split_name_004(self):
		parser_obj = Parser.__new__(Parser)
		full_name = 'First Name //'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', ''))

	def test_split_name_005(self):
		parser_obj = Parser.__new__(Parser)
		full_name = 'First Name /Last Name'

		split_name = parser_obj.splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

if __name__ == '__main__':
	unittest.main()
