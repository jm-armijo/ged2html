import unittest
from unittest.mock import MagicMock, Mock
from ..person import Person
from ..html import HTMLGenerator

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
		self.assertEqual(person.parents, None)
		self.assertEqual(person.unions, list())

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
		person._splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person._splitName.assert_called_with(full_name)
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
		person._splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person._splitName.assert_called_with(full_name)
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
		person._splitName = MagicMock(return_value=[given_name, last_name])
		person.setGivenName = MagicMock()

		# Actual test
		person.setName(full_name)
		person._splitName.assert_called_with(full_name)
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
	# Person.set_sex
	##########################################

	def test_set_sex(self):
		person = Person.__new__(Person)
		sex = 'M'
		person.set_sex(sex)
		self.assertEqual(person.sex, sex)

	##########################################
	# Person.set_birth_date
	##########################################

	def test_set_birth_date(self):
		person = Person.__new__(Person)
		date = '19 DEC 1800'
		person.set_birth_date(date)
		self.assertEqual(person.birth_date, date)

	##########################################
	# Person.set_birth_place
	##########################################

	def test_set_birth_place(self):
		person = Person.__new__(Person)
		place = 'Town, City, Country'
		person.set_birth_place(place)
		self.assertEqual(person.birth_place, place)

	##########################################
	# Person.set_death_date
	##########################################

	def test_set_death_date(self):
		person = Person.__new__(Person)
		date = '19 DEC 1800'
		person.set_death_date(date)
		self.assertEqual(person.death_date, date)

	##########################################
	# Person.set_death_place
	##########################################

	def test_set_death_place(self):
		person = Person.__new__(Person)
		place = 'Town, City, Country'
		person.set_death_place(place)
		self.assertEqual(person.death_place, place)

	##########################################
	# Person.setParents
	##########################################

	def test_set_parent_union_001(self):
		person = Person.__new__(Person)
		person.parents = None
		parents = Mock()
		person.setParents(parents)
		self.assertEqual(person.parents, parents)

	##########################################
	# Person.addUnion
	##########################################

	def test_add_union_001(self):
		person = Person.__new__(Person)
		person.unions = list()
		union = Mock()
		person.addUnion(union)
		self.assertEqual(person.unions[0], union)

	def test_add_union_002(self):
		person = Person.__new__(Person)
		person.unions = [Mock()]
		union = Mock()
		person.addUnion(union)
		self.assertEqual(person.unions[1], union)

	##########################################
	# Person.getChildren
	##########################################

	def test_get_children_001(self):
		person = Person.__new__(Person)
		person.unions = list()

		returned_children = person.getChildren()
		self.assertEqual(returned_children, list())

	def test_get_children_002(self):
		children = [Mock(), Mock()]
		union = Mock()
		union.getChildren = MagicMock(return_value = children)

		person = Person.__new__(Person)
		person.unions = [union]

		returned_children = person.getChildren()
		self.assertEqual(returned_children, children)

	def test_get_children_003(self):
		children1 = [Mock(), Mock()]
		children2 = [Mock(), Mock()]
		union1 = Mock()
		union2 = Mock()
		union1.getChildren = MagicMock(return_value = children1)
		union2.getChildren = MagicMock(return_value = children2)

		person = Person.__new__(Person)
		person.unions = [union1, union2]

		returned_children = person.getChildren()
		self.assertEqual(returned_children, children1 + children2)

	##########################################
	# Person.getParents
	##########################################

	def test_get_parents_001(self):
		person = Person.__new__(Person)
		person.parents = None

		returned_parents = person.getParents()
		self.assertEqual(returned_parents, list())

	def test_get_parents_002(self):
		parents = Mock()
		person = Person.__new__(Person)
		person.parents = parents

		returned_parents = person.getParents()
		self.assertEqual(returned_parents, [parents])

	##########################################
	# Person.getUnions
	##########################################

	def test_get_unions_001(self):
		unions = []
		person = Person.__new__(Person)
		person.unions = unions

		returned_unions = person.getUnions()
		self.assertEqual(returned_unions, unions)

	def test_get_unions_002(self):
		unions = [Mock(), Mock()]
		person = Person.__new__(Person)
		person.unions = unions

		returned_unions = person.getUnions()
		self.assertEqual(returned_unions, unions)

	##########################################
	# Person.isSingle()
	##########################################

	def test_is_single_001(self):
		person = Person.__new__(Person)
		person.unions = list()

		single = person.isSingle()
		self.assertTrue(single)

	##########################################
	# Person.toHTML()
	##########################################

	def test_to_html_001(self):
		person = Person.__new__(Person)
		person.unions = list()
		person.id = '@I000001@'
		person.given_name = 'Given'
		person.last_name = 'Last'
		person.birth_date = '01-01-1900'
		person.death_date = '31-12-1999'

		value = (
			'  <div class="given">Given</div>\n'
			'  <div class="last">Last</div>\n'
			'  <div class="dates">01-01-1900 - 31-12-1999</div>\n'
		)

		wrapped = "<div>"+value+"</div>"
		HTMLGenerator.wrap = MagicMock(return_value = wrapped)

		html = person.toHTML()
		HTMLGenerator.wrap.assert_called_once_with(person, value, person.id)
		self.assertEqual(wrapped, html)

	def test_to_html_002(self):
		person = Person.__new__(Person)
		person.unions = list()
		person.id = '@I000001@'
		person.given_name = 'Given'
		person.last_name = 'Last'
		person.birth_date = '01-01-1900'
		person.death_date = ''

		value = (
			'  <div class="given">Given</div>\n'
			'  <div class="last">Last</div>\n'
			'  <div class="dates">01-01-1900 - </div>\n'
		)

		wrapped = "<div>"+value+"</div>"
		HTMLGenerator.wrap = MagicMock(return_value = wrapped)

		html = person.toHTML()
		HTMLGenerator.wrap.assert_called_once_with(person, value, person.id)
		self.assertEqual(wrapped, html)

	def test_to_html_003(self):
		person = Person.__new__(Person)
		person.unions = list()
		person.id = '@I000001@'
		person.given_name = ''
		person.last_name = 'Last'
		person.birth_date = '01-01-1900'
		person.death_date = ''

		value = (
			'  <div class="given"></div>\n'
			'  <div class="last">Last</div>\n'
			'  <div class="dates">01-01-1900 - </div>\n'
		)

		wrapped = "<div>"+value+"</div>"
		HTMLGenerator.wrap = MagicMock(return_value = wrapped)

		html = person.toHTML()
		HTMLGenerator.wrap.assert_called_once_with(person, value, person.id)
		self.assertEqual(wrapped, html)

	##########################################
	# Person._splitName
	##########################################

	def test_split_name_001(self):
		person = Person.__new__(Person)
		full_name = 'First Name /Last Name/'

		split_name = person._splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_002(self):
		person = Person.__new__(Person)
		full_name = '     First Name    /    Last Name   /   '

		split_name = person._splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	def test_split_name_003(self):
		person = Person.__new__(Person)
		full_name = '/Last Name/'

		split_name = person._splitName(full_name)
		self.assertEqual(split_name, ('', 'Last Name'))

	def test_split_name_004(self):
		person = Person.__new__(Person)
		full_name = 'First Name //'

		split_name = person._splitName(full_name)
		self.assertEqual(split_name, ('First Name', ''))

	def test_split_name_005(self):
		person = Person.__new__(Person)
		full_name = 'First Name /Last Name'

		split_name = person._splitName(full_name)
		self.assertEqual(split_name, ('First Name', 'Last Name'))

	##########################################
	# Person.__str__
	##########################################

	def test_str_001(self):
		person = Person.__new__(Person)
		person.id = "@I1234567@"
		person.given_name = 'First Name'
		person.last_name = 'Last Name'
		person.sex = ''
		person.birth_date = ''
		person.birth_place = ''
		person.death_date = ''
		person.death_place = ''
		person.parents = None
		person.unions = list()

		self.assertEqual(str(person), "[First Name Last Name]")

if __name__ == '__main__':
	unittest.main()
