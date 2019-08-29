import unittest
from ..null_person import NullPerson

class TestNullPerson(unittest.TestCase):

	##########################################
	# TreeNullPerson.toHTML
	##########################################

	def test_to_html_001(self):
		html = '<div class="person"></div>'
		null_person = NullPerson.__new__(NullPerson)

		return_value = null_person.toHTML()
		self.assertEqual(return_value, html)

	##########################################
	# TreeNullPerson.getUnions
	##########################################

	def test_get_unions_001(self):
		unions = list()
		null_person = NullPerson.__new__(NullPerson)

		return_value = null_person.getUnions()
		self.assertEqual(return_value, unions)

if __name__ == '__main__':
	unittest.main()
