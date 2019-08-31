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
	# Parser.makeTree
	##########################################

	@patch("src.tree.Tree.__new__")
	def test_make_tree_001(self, class_tree):
		# Setup data
		file_name = 'file.ged'
		tree = Mock()
		lines = Mock()
		class_tree.return_value = tree

		# Setup Parser
		parser = Parser.__new__(Parser)
		parser._readFile = MagicMock(return_value = lines)
		parser.parseLines = MagicMock()
		parser.people = dict()
		parser.unions = list()

		# Actual test
		returned_tree = parser.makeTree(file_name)
		parser._readFile.assert_called_once_with(file_name)
		parser.parseLines.assert_called_once_with(lines)
		self.assertEqual(returned_tree, tree)

	@patch("src.tree.Tree.__new__")
	def test_make_tree_002(self, class_tree):
		# Setup data
		file_name = 'file.ged'
		lines = Mock()
		tree = Mock()
		class_tree.return_value = tree

		# Setup people
		people = {'@I000123':Mock()}

		# Setup Parser
		parser = Parser.__new__(Parser)
		parser._readFile = MagicMock(return_value = lines)
		parser.parseLines = MagicMock()
		parser.people = people
		parser.unions = list()

		# Actual test
		returned_tree = parser.makeTree(file_name)
		parser._readFile.assert_called_once_with(file_name)
		parser.parseLines.assert_called_once_with(lines)
		self.assertEqual(returned_tree, tree)

	##########################################
	# Parser.parse_lines
	##########################################

	def test_parse_lines_001(self):
		# Setup
		lines = [Mock(), Mock(), Mock()]
		parser = Parser.__new__(Parser)
		parser.people = dict()
		parser.unions = dict()
		parser.last_key_per_level = dict()
		parser.getCurrentState = MagicMock()
		parser.parseCurrentLine = MagicMock()

		# Actual test
		parser.parseLines(lines)
		self.assertEqual(parser.getCurrentState.call_count, len(lines))
		self.assertEqual(parser.parseCurrentLine.call_count, len(lines))

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
	# Parser.parse_current_line
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

	##########################################
	# Parser.addPersonData
	##########################################

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
		person.set_sex= MagicMock()

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
		person.set_sex.assert_called_with(line.data)

	def test_add_person_data_004(self):
		# Setup person
		person = Mock()
		person.id = '@I000123@'
		person.set_birth_date = MagicMock()

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
		person.set_birth_date.assert_called_with(line.data)

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
		person.set_sex= MagicMock()
		person.set_birth_date= MagicMock()
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
		person.set_sex= MagicMock()
		person.set_birth_date= MagicMock()
		person.setBirthPlace= MagicMock()

	##########################################
	# Parser.createUnion
	##########################################

	@patch("src.union.Union.__new__")
	def test_create_union_001(self, mock_union):
		union = Mock()
		mock_union.return_value = union

		attribute = Mock()
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()
		parser.current_line.attribute = attribute
		parser.unions = list()

		parser.createUnion()
		mock_union.assert_called_with(ANY, attribute)
		self.assertEqual(parser.unions, [union])

	@patch("src.union.Union.__new__")
	def test_create_union_002(self, mock_union):
		union1 = Mock()
		union2 = Mock()
		mock_union.return_value = union2

		attribute = Mock()
		parser = Parser.__new__(Parser)
		parser.current_line = Mock()
		parser.current_line.attribute = attribute
		parser.unions = [union1]

		parser.createUnion()
		mock_union.assert_called_with(ANY, attribute)
		self.assertEqual(parser.unions, [union1, union2])

	##########################################
	# Parser.addUnionData
	##########################################

	def test_add_union_data_001(self):
		attribute = 'HUSB'
		value = '@I0001@'
		person = Mock()

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock(return_value = person)

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_called_once_with(value)
		union1.setSpouse1.assert_called_once_with(person)
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_not_called()
		union1.setDate.assert_not_called()
		union1.setPlace.assert_not_called()

	def test_add_union_data_002(self):
		attribute = 'WIFE'
		value = '@I0002@'
		person = Mock()

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock(return_value = person)

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_called_once_with(value)
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_called_once_with(person)
		union1.addChild.assert_not_called()
		union1.setDate.assert_not_called()
		union1.setPlace.assert_not_called()

	def test_add_union_data_003(self):
		attribute = 'CHIL'
		value = '@I0003@'
		person = Mock()

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock(return_value = person)

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_called_once_with(value)
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_called_once_with(person)
		union1.setDate.assert_not_called()
		union1.setPlace.assert_not_called()

	def test_add_union_data_004(self):
		attribute = 'DATE'
		value = '01-02-1900'

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock()
		parser.last_key_per_level = {0: 'MARR'}

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_not_called()
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_not_called()
		union1.setDate.assert_called_once_with(value)
		union1.setPlace.assert_not_called()

	def test_add_union_data_005(self):
		attribute = 'DATE'
		value = '01-02-1900'

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock()
		parser.last_key_per_level = {0: 'ANY'}

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_not_called()
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_not_called()
		union1.setDate.assert_not_called()
		union1.setPlace.assert_not_called()

	def test_add_union_data_006(self):
		attribute = 'PLAC'
		value = 'Somewhere'

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock()
		parser.last_key_per_level = {0: 'MARR'}

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_not_called()
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_not_called()
		union1.setDate.assert_not_called()
		union1.setPlace.assert_called_once_with(value)

	def test_add_union_data_007(self):
		attribute = 'PLAC'
		value = 'Somewhere'

		# Setup line
		line = Mock()
		line.level = 1
		line.attribute = attribute
		line.data = value

		# Setup parser
		parser = Parser.__new__(Parser)
		parser.current_line = line
		parser.getPersonOrCreate = MagicMock()
		parser.last_key_per_level = {0: 'ANY'}

		# Setup parser unions
		union1 = Mock()
		union1.setSpouse1 = MagicMock()
		union1.setSpouse2 = MagicMock()
		union1.addChild = MagicMock()
		union1.setDate = MagicMock()
		union1.setPlace = MagicMock()
		parser.unions = [union1]

		# Actual test
		parser.addUnionData()
		parser.getPersonOrCreate.assert_not_called()
		union1.setSpouse1.assert_not_called()
		union1.setSpouse2.assert_not_called()
		union1.addChild.assert_not_called()
		union1.setDate.assert_not_called()
		union1.setPlace.assert_not_called()

	##########################################
	# Parser.getPersonOrCreate
	##########################################

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
if __name__ == '__main__':
	unittest.main()
