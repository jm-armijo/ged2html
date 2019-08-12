import unittest
from unittest.mock import Mock, MagicMock, call, ANY, patch
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
		parser = Parser.__new__(Parser)
		parser.people = dict()
		parser.unions = dict()
		parser.last_key_per_level = dict()

		# Actual test
		people = parser.parseLines(lines)
		self.assertEqual(mock_get.call_count, len(lines))
		self.assertEqual(mock_parse.call_count, len(lines))
		self.assertEqual(people, parser.people)

	##########################################
	# Parser.get_current_state
	##########################################

	# From any state goes to INDI when level = 0
	def test_get_current_state_001(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser.current_line.level = 0
		parser.current_line.data = 'INDI'

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'INDI')

	# From any state goes to FAM when level = 0
	def test_get_current_state_002(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser.current_line.level = 0
		parser.current_line.data = 'FAM'

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'FAM')

	# Stays on IDLE if level > 0
	def test_get_current_state_003(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser.state = 'IDLE'
		parser.current_line.level = 1

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From FAM goes to IDLE if no more data
	def test_get_current_state_004(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser.state = 'FAM'
		parser.current_line.level = 0
		parser.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to IDLE if no more data
	def test_get_current_state_005(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser.state = 'INDI'
		parser.current_line.level = 0
		parser.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to INDI_DATA (level 1)
	def test_get_current_state_006(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser.current_line = Mock()
		parser.current_line.level = 1

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI goes to INDI_DATA (level 9999)
	def test_get_current_state_007(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser.current_line = Mock()
		parser.current_line.level = 9999

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 1)
	def test_get_current_state_008(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'INDI_DATA'
		parser.current_line = Mock()
		parser.current_line.level = 1

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 9999)
	def test_get_current_state_009(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'INDI_DATA'
		parser.current_line = Mock()
		parser.current_line.level = 9999

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From FAM goes to FAM_DATA (level 1)
	def test_get_current_state_010(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser.current_line = Mock()
		parser.current_line.level = 1

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM goes to FAM_DATA (level 9999)
	def test_get_current_state_011(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser.current_line = Mock()
		parser.current_line.level = 9999

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 1)
	def test_get_current_state_012(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'FAM_DATA'
		parser.current_line = Mock()
		parser.current_line.level = 1

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 9999)
	def test_get_current_state_013(self):
		# Setup
		parser = Parser.__new__(Parser)
		parser.state = 'FAM_DATA'
		parser.current_line = Mock()
		parser.current_line.level = 9999

		# Actual test
		new_state = parser.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	##########################################
	# Parser.get_current_line
	##########################################

	def test_parse_current_line_001(self):
		parser = Parser.__new__(Parser)
		parser.state = 'INDI'

		# Mock parser functions
		parser.createPerson = MagicMock()
		parser.addPersonData = MagicMock()
		parser.createUnion = MagicMock()
		parser.addUnionData = MagicMock()

		# Actual test
		parser.parseCurrentLine()
		parser.createPerson.assert_called()
		parser.addPersonData.assert_not_called()
		parser.createUnion.assert_not_called()
		parser.addUnionData.assert_not_called()

	def test_parse_current_line_002(self):
		parser = Parser.__new__(Parser)
		parser.state = 'INDI_DATA'

		# Mock parser functions
		parser.createPerson = MagicMock()
		parser.addPersonData = MagicMock()
		parser.createUnion = MagicMock()
		parser.addUnionData = MagicMock()

		# Actual test
		parser.parseCurrentLine()
		parser.createPerson.assert_not_called()
		parser.addPersonData.assert_called()
		parser.createUnion.assert_not_called()
		parser.addUnionData.assert_not_called()

	def test_parse_current_line_003(self):
		parser = Parser.__new__(Parser)
		parser.state = 'FAM'

		# Mock parser functions
		parser.createPerson = MagicMock()
		parser.addPersonData = MagicMock()
		parser.createUnion = MagicMock()
		parser.addUnionData = MagicMock()

		# Actual test
		parser.parseCurrentLine()
		parser.createPerson.assert_not_called()
		parser.addPersonData.assert_not_called()
		parser.createUnion.assert_called()
		parser.addUnionData.assert_not_called()

	def test_parse_current_line_004(self):
		parser = Parser.__new__(Parser)
		parser.state = 'FAM_DATA'

		# Mock parser functions
		parser.createPerson = MagicMock()
		parser.addPersonData = MagicMock()
		parser.createUnion = MagicMock()
		parser.addUnionData = MagicMock()

		# Actual test
		parser.parseCurrentLine()
		parser.createPerson.assert_not_called()
		parser.addPersonData.assert_not_called()
		parser.createUnion.assert_not_called()
		parser.addUnionData.assert_called()

	def test_parse_current_line_005(self):
		parser = Parser.__new__(Parser)
		parser.state = 'IDLE'

		# Mock parser functions
		parser.createPerson = MagicMock()
		parser.addPersonData = MagicMock()
		parser.createUnion = MagicMock()
		parser.addUnionData = MagicMock()

		# Actual test
		parser.parseCurrentLine()
		parser.createPerson.assert_not_called()
		parser.addPersonData.assert_not_called()
		parser.createUnion.assert_not_called()
		parser.addUnionData.assert_not_called()

	##########################################
	# Parser.createPerson
	##########################################

	@patch("src.person.Person.__new__")
	def test_create_person_001(self, mock):
		# Setup person
		person_id = '@I000123@'
		person = Mock()
		person.id = person_id

		# Mock person constructor
		mock.return_value = person

		# Setup line
		line = Mock()
		line.attribute = person_id

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.last_person = person_id
		parser.people = dict()

		# Test that Person constructor is called with right arguments
		parser.createPerson()
		self.assertEqual(mock.call_count, 1)
		args = mock.call_args[0]
		self.assertEqual(args[1], line.attribute)
		self.assertEqual(len(args), 2)

		# Teset that the new person is added to the people dictionary
		self.assertEqual(len(parser.people), 1)
		self.assertEqual(parser.people[person.id], person)

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

		person1.id = person1_id
		person2.id = person2_id
		person3.id = person3_id

		# Mock person
		mock.side_effect = [person1, person2, person3]

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.last_person = None
		parser.people = dict()

		# Create Person 1
		line = Mock()
		line.attribute = person1_id
		parser.current_line = line
		parser.createPerson()

		# Create Person 2
		line = Mock()
		line.attribute = person2_id
		parser.current_line = line
		parser.createPerson()

		# Create Person 3
		line = Mock()
		line.attribute = person3_id
		parser.current_line = line
		parser.createPerson()

		# Test that Person constructor is called with right arguments
		self.assertEqual(mock.call_count, 3)

		args = mock.call_args_list[0][0]
		self.assertEqual(args[1], person1_id)
		self.assertEqual(len(args), 2)

		args = mock.call_args_list[1][0]
		self.assertEqual(args[1], person2_id)
		self.assertEqual(len(args), 2)

		args = mock.call_args_list[2][0]
		self.assertEqual(args[1], person3_id)
		self.assertEqual(len(args), 2)

		# Test that the new person is added to the people dictionary
		self.assertEqual(len(parser.people), 3)
		self.assertEqual(parser.people[person3.id], person3)
		self.assertEqual(parser.people[person2.id], person2)
		self.assertEqual(parser.people[person1.id], person1)

	'''
	When creating Person objects with duplicated values, the duplicated replaces the original
	'''
	def test_create_person_003(self):
		# Setup people
		dup_id = '@I000123@'
		person3_id = '@I000323@'

		person1 = Mock()
		person2 = Mock()
		person3 = Mock()

		person1.id = dup_id
		person2.id = dup_id
		person3.id = person3_id

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.last_person = None
		parser.people = dict()
		parser.getPersonOrCreate = MagicMock(side_effect = [person1, person2, person3])

		# Create Person 1
		line = Mock()
		line.attribute = dup_id
		parser.current_line = line
		parser.createPerson()

		# Create Person 2
		line = Mock()
		line.attribute = dup_id
		parser.current_line = line
		parser.createPerson()

		# Create Person 3
		line = Mock()
		line.attribute = person3_id
		parser.current_line = line
		parser.createPerson()


		# Test that Person constructor is called with right arguments
		self.assertEqual(parser.getPersonOrCreate.call_count,3)
		self.assertEqual(parser.getPersonOrCreate.mock_calls, [call(dup_id), call(dup_id), call(person3_id)])

		# Test that the new persons are added to the people dictionary
		self.assertEqual(len(parser.people), 2)
		self.assertEqual(parser.people[person3.id], person3)
		self.assertEqual(parser.people[dup_id], person2)

	###########################################
	## Parser.getPersonOrCreate
	###########################################

	@patch("src.person.Person.__new__")
	def test_get_person_or_create_001(self, mock_person):
		id = '@I001234@'
		parser = Parser.__new__(Parser)
		parser.people = dict()

		parser.getPersonOrCreate(id)
		mock_person.assert_called_with(ANY, id)

	@patch("src.person.Person.__new__")
	def test_get_person_or_create_002(self, mock_person):
		id = '@I001234@'
		parser = Parser.__new__(Parser)
		parser.people = {id: Mock()}

		parser.getPersonOrCreate(id)
		mock_person.assert_not_called()

	###########################################
	## Parser.addPersonData
	###########################################

	def test_add_person_data_001(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setName = MagicMock()

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = 'NAME'
		line.data = 'First /Last'

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id

		# Actual test
		parser.addPersonData()
		person.setName.assert_called_with(line.data)

	def test_add_person_data_002(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setGivenName = MagicMock()

		# Setup line
		line = Mock()
		line.level = 2
		line.attribute = 'GIVN'
		line.data = 'First'

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id

		# Actual test
		parser.addPersonData()
		person.setGivenName.assert_called_with(line.data)

	def test_add_person_data_003(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setSex= MagicMock()

		# Setup line
		line = Mock()
		line.attribute = 'SEX'
		line.level = 1
		line.data = 'F'

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id

		# Actual test
		parser.addPersonData()
		person.setSex.assert_called_with(line.data)

	def test_add_person_data_004(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setBirthDate= MagicMock()

		# Setup line
		line = Mock()
		line.attribute = 'DATE'
		line.level = 2
		line.data = 'F'

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id
		parser.last_key_per_level = {1: 'BIRT'}

		# Actual test
		parser.addPersonData()
		person.setBirthDate.assert_called_with(line.data)

	def test_add_person_data_005(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setBirthPlace= MagicMock()

		# Setup line
		line = Mock()
		line.attribute = 'PLAC'
		line.level = 2
		line.data = 'Town, City, Country'

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id
		parser.last_key_per_level = {1: 'BIRT'}

		# Actual test
		parser.addPersonData()
		person.setBirthPlace.assert_called_with(line.data)

	def test_add_person_data_006(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.setName = MagicMock()
		person.setGivenName = MagicMock()
		person.setSex= MagicMock()
		person.setBirthDate= MagicMock()
		person.setBirthPlace= MagicMock()

		# Setup line
		line = Mock()
		line.attribute = 'KEY'
		line.level = '2'
		line.data = "Some data"

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.people = {person.id: person}
		parser.last_person = person.id

		# Actual test
		parser.addPersonData()
		person.setName.assert_not_called()
		person.setGivenName.assert_not_called()
		person.setSex= MagicMock()
		person.setBirthDate= MagicMock()
		person.setBirthPlace= MagicMock()

if __name__ == '__main__':
	unittest.main()
