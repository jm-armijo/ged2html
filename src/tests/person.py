import unittest
from unittest.mock import MagicMock
from ..person import Person

class TestPerson(unittest.TestCase):
	##########################################
	# Person.init
	##########################################

	def test_init_001(self):
		id = "@I1234567@"
		person = Person(id)
		self.assertEqual(person.id, id)
		self.assertEqual(person.given_name, '')
		self.assertEqual(person.last_name, '')
		self.assertEqual(person.sex, '')
		self.assertEqual(person.birth_date, '')
		self.assertEqual(person.birth_place, '')
		self.assertEqual(person.death_date, '')
		self.assertEqual(person.death_place, '')

	##########################################
	# Person.setName
	##########################################

	def test_set_name_001(self):
		# Setup name
		given_name = 'Given Name'
		last_name = 'Last Name'
		full_name = "{} /{}/".format(given_name, last_name)

		# Mock person
		person = Person.__new__(Person)
		person.given_name = ''
		person.splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person.splitName.assert_called_with(full_name)
		person.setGivenName.assert_called_with(given_name)
		self.assertEqual(person.last_name, last_name)

	def test_set_name_002(self):
		# Setup name
		given_name = 'Given Name'
		last_name = 'Last Name'
		full_name = "{} /{}/".format(given_name, last_name)

		# Mock person
		person = Person.__new__(Person)
		person.given_name = 'A name'
		person.splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person.splitName.assert_called_with(full_name)
		person.setGivenName.assert_called_with(given_name)
		self.assertEqual(person.last_name, last_name)

	def test_set_name_003(self):
		# Setup name
		given_name = ''
		last_name = ''
		full_name = "{} /{}/".format(given_name, last_name)

		# Mock person
		person = Person.__new__(Person)
		person.given_name = ''
		person.splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person.splitName.assert_called_with(full_name)
		person.setGivenName.assert_called_with(given_name)
		self.assertEqual(person.last_name, last_name)

	##########################################
	# Person.setGivenName
	##########################################

	def test_set_given_name_001(self):
		# Setup name
		old_given_name = ''
		new_given_name = ''

		# Mock person
		person = Person.__new__(Person)
		person.given_name = old_given_name

		# Actual test
		person.setGivenName(new_given_name)
		self.assertEqual(person.given_name, new_given_name)

	def test_set_given_name_002(self):
		# Setup name
		old_given_name = ''
		new_given_name = 'New Given Name'

		# Mock person
		person = Person.__new__(Person)
		person.given_name = old_given_name

		# Actual test
		person.setGivenName(new_given_name)
		self.assertEqual(person.given_name, new_given_name)

	def test_set_given_name_003(self):
		# Setup name
		old_given_name = 'Existing Given Name'
		new_given_name = ''

		# Mock person
		person = Person.__new__(Person)
		person.given_name = old_given_name

		# Actual test
		person.setGivenName(new_given_name)
		self.assertEqual(person.given_name, old_given_name)

	def test_set_given_name_004(self):
		# Setup name
		old_given_name = 'Existing Given Name'
		new_given_name = 'New Given Name'

		# Mock person
		person = Person.__new__(Person)
		person.given_name = old_given_name

		# Actual test
		person.setGivenName(new_given_name)
		self.assertEqual(person.given_name, old_given_name)

	##########################################
	# Person.setSex
	##########################################

	def test_set_sex(self):
		person = Person.__new__(Person)
		sex = 'M'
		person.setSex(sex)
		self.assertEqual(person.sex, sex)

	##########################################
	# Person.setBirthDate
	##########################################

	def test_set_birth_date(self):
		person = Person.__new__(Person)
		date = '19 DEC 1800'
		person.setBirthDate(date)
		self.assertEqual(person.birth_date, date)

	##########################################
	# Person.setBirthPlace
	##########################################

	def test_set_birth_place(self):
		person = Person.__new__(Person)
		place = 'Town, City, Country'
		person.setBirthPlace(place)
		self.assertEqual(person.birth_place, place)

	##########################################
	# Person.setDeathDate
	##########################################

	def test_set_death_date(self):
		person = Person.__new__(Person)
		date = '19 DEC 1800'
		person.setDeadthDate(date)
		self.assertEqual(person.death_date, date)

	##########################################
	# Person.setDeathPlace
	##########################################

	def test_set_death_place(self):
		person = Person.__new__(Person)
		place = 'Town, City, Country'
		person.setDeadthPlace(place)
		self.assertEqual(person.death_place, place)

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
