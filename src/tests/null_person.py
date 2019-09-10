import unittest
from ..null_person import NullPerson

class TestNullPerson(unittest.TestCase):

    ##########################################
    # NullPerson.to_html
    ##########################################

    def test_to_html_001(self):
        html = '<div class="person"></div>'
        null_person = NullPerson.__new__(NullPerson)

        return_value = null_person.to_html()
        self.assertEqual(return_value, html)

    ##########################################
    # NullPerson.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = list()
        null_person = NullPerson.__new__(NullPerson)

        return_value = null_person.get_unions()
        self.assertEqual(return_value, unions)

if __name__ == '__main__':
    unittest.main()
