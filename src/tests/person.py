import unittest
from unittest.mock import MagicMock, Mock, patch, ANY, call
from ..person import Person
from ..html import HTMLGenerator

class TestPerson(unittest.TestCase):
    ##########################################
    # Person.init
    ##########################################

    @patch("src.date_range.DateRange.__new__")
    def test_init_001(self, class_date_range):
        date_range = Mock()
        class_date_range.return_value = date_range

        id = "@I1234567@"
        person = Person(id)
        self.assertEqual(person.id, id)
        self.assertEqual(person.first_name, '')
        self.assertEqual(person.last_name, '')
        self.assertEqual(person.sex, 'U')
        self.assertEqual(person.life_period, date_range)
        self.assertEqual(person.birth_place, '')
        self.assertEqual(person.death_place, '')
        self.assertEqual(person.parents, list())
        self.assertEqual(person.unions, list())

    @patch("src.date_range.DateRange.__new__")
    def test_init_002(self, class_date_range):
        date_range = Mock()
        class_date_range.return_value = date_range

        person = Person()
        self.assertEqual(person.id, '')
        self.assertEqual(person.first_name, '')
        self.assertEqual(person.last_name, '')
        self.assertEqual(person.sex, 'U')
        self.assertEqual(person.life_period, date_range)
        self.assertEqual(person.birth_place, '')
        self.assertEqual(person.death_place, '')
        self.assertEqual(person.parents, list())
        self.assertEqual(person.unions, list())

    ##########################################
    # Person.set_name
    ##########################################

    def test_set_name_001(self):
        # Setup name
        first_name = 'Given Name'
        last_name = 'Last Name'
        full_name = "{} /{}/".format(first_name, last_name)

        # Mock person
        person = Person.__new__(Person)
        person.first_name = ''
        person._split_name = MagicMock(return_value=[first_name, last_name])
        person.set_given_name = MagicMock()

        # Actual test
        person.set_name(full_name)
        person._split_name.assert_called_with(full_name)
        person.set_given_name.assert_called_with(first_name)
        self.assertEqual(person.last_name, last_name.lower())

    def test_set_name_002(self):
        # Setup name
        first_name = 'Given Name'
        last_name = 'Last Name'
        full_name = "{} /{}/".format(first_name, last_name)

        # Mock person
        person = Person.__new__(Person)
        person.first_name = 'A name'
        person._split_name = MagicMock(return_value=[first_name, last_name])
        person.set_given_name = MagicMock()

        # Actual test
        person.set_name(full_name)
        person._split_name.assert_called_with(full_name)
        person.set_given_name.assert_called_with(first_name)
        self.assertEqual(person.last_name, last_name.lower())

    def test_set_name_003(self):
        # Setup name
        first_name = ''
        last_name = ''
        full_name = "{} /{}/".format(first_name, last_name)

        # Mock person
        person = Person.__new__(Person)
        person.first_name = ''
        person._split_name = MagicMock(return_value=[first_name, last_name])
        person.set_given_name = MagicMock()

        # Actual test
        person.set_name(full_name)
        person._split_name.assert_called_with(full_name)
        person.set_given_name.assert_called_with(first_name)
        self.assertEqual(person.last_name, last_name)

    ##########################################
    # Person.set_given_name
    ##########################################

    def test_set_given_name_001(self):
        # Setup name
        old_first_name = ''
        new_first_name = ''

        # Mock person
        person = Person.__new__(Person)
        person.first_name = old_first_name

        # Actual test
        person.set_given_name(new_first_name)
        self.assertEqual(person.first_name, new_first_name)

    def test_set_given_name_002(self):
        # Setup name
        old_first_name = ''
        new_first_name = 'New Given Name'

        # Mock person
        person = Person.__new__(Person)
        person.first_name = old_first_name

        # Actual test
        expected = new_first_name.lower()
        person.set_given_name(new_first_name)
        self.assertEqual(person.first_name, expected)

    def test_set_given_name_003(self):
        # Setup name
        old_first_name = 'Existing Given Name'
        new_first_name = ''

        # Mock person
        person = Person.__new__(Person)
        person.first_name = old_first_name

        # Actual test
        expected = old_first_name
        person.set_given_name(new_first_name)
        self.assertEqual(person.first_name, expected)

    def test_set_given_name_004(self):
        # Setup name
        old_first_name = 'Existing Given Name'
        new_first_name = 'New Given Name'

        # Mock person
        person = Person.__new__(Person)
        person.first_name = old_first_name

        # Actual test
        person.set_given_name(new_first_name)
        self.assertEqual(person.first_name, old_first_name)

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
        person.life_period = Mock()

        date = '19 DEC 1800'
        person.set_birth_date(date)
        self.assertEqual(person.life_period.start, date)

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
        person.life_period = Mock()

        date = '19 DEC 1800'
        person.set_death_date(date)
        self.assertEqual(person.life_period.end, date)

    ##########################################
    # Person.set_death_place
    ##########################################

    def test_set_death_place(self):
        person = Person.__new__(Person)
        place = 'Town, City, Country'
        person.set_death_place(place)
        self.assertEqual(person.death_place, place)

    ##########################################
    # Person.set_parents
    ##########################################

    def test_set_parent_union_001(self):
        person = Person.__new__(Person)
        person.parents = list()
        parents = Mock()
        person.set_parents(parents)
        self.assertEqual(person.parents, [parents])

    ##########################################
    # Person.add_union
    ##########################################

    def test_add_union_001(self):
        person = Person.__new__(Person)
        person.unions = list()
        person.children = list()

        child1 = Mock()
        children = [child1]

        union = Mock()
        union.get_children = MagicMock(return_value = children)

        person.add_union(union)
        self.assertEqual(person.unions[0], union)
        self.assertEqual(person.children[0], child1)

    def test_add_union_002(self):
        children = [Mock()]

        union = Mock()
        union.get_children = MagicMock(return_value = children)

        person = Person.__new__(Person)
        person.unions = [Mock()]
        person.children = list()

        person.add_union(union)
        self.assertEqual(person.unions[1], union)
        self.assertEqual(person.children, children)

    ##########################################
    # Person.get_spouses
    ##########################################

    def test_get_spouses_001(self):
        person = Person.__new__(Person)

        expected = [person]
        actual = person.get_spouses()
        self.assertEqual(expected, actual)

    ##########################################
    # Person.get_children
    ##########################################

    def test_get_children_001(self):
        children = list()

        person = Person.__new__(Person)
        person.children = children

        returned_children = person.get_children()
        self.assertEqual(returned_children, children)

    def test_get_children_002(self):
        children = [Mock(), Mock()]

        person = Person.__new__(Person)
        person.children = children

        returned_children = person.get_children()
        self.assertEqual(returned_children, children)

    def test_get_children_003(self):
        children1 = [Mock(), Mock()]
        children2 = [Mock(), Mock()]
        children = children1 + children2

        person = Person.__new__(Person)
        person.children = children

        returned_children = person.get_children()
        self.assertEqual(returned_children, children)

    ##########################################
    # Person.get_parents
    ##########################################

    def test_get_parents_001(self):
        person = Person.__new__(Person)
        person.parents = list()

        returned_parents = person.get_parents()
        self.assertEqual(returned_parents, list())

    def test_get_parents_002(self):
        parents = [Mock()]
        person = Person.__new__(Person)
        person.parents = parents

        returned_parents = person.get_parents()
        self.assertEqual(returned_parents, parents)

    ##########################################
    # Person.get_unions
    ##########################################

    def test_get_unions_001(self):
        unions = []
        person = Person.__new__(Person)
        person.unions = unions

        returned_unions = person.get_unions()
        self.assertEqual(returned_unions, unions)

    def test_get_unions_002(self):
        unions = [Mock(), Mock()]
        person = Person.__new__(Person)
        person.unions = unions

        returned_unions = person.get_unions()
        self.assertEqual(returned_unions, unions)

    ##########################################
    # Person.is_single()
    ##########################################

    def test_is_single_001(self):
        person = Person.__new__(Person)
        person.unions = list()

        single = person.is_single()
        self.assertTrue(single)

    ##########################################
    # Person.to_html()
    ##########################################

    def test_to_html_001(self):
        person = Person.__new__(Person)
        person._image_to_html = MagicMock(return_value='<div>image</div>')
        person._info_to_html = MagicMock(return_value='<div>info</div>')
        person.id = '@I000001@'

        value = (
            '  <div>image</div>'
            '  <div>info</div>'
        )

        expected = "<div>"+value+"</div>"
        HTMLGenerator.wrap_instance = MagicMock(return_value = expected)

        actual = person.to_html()
        HTMLGenerator.wrap_instance.assert_called_once_with(person, value, person.id)
        self.assertEqual(actual, expected)

    ##########################################
    # Person._info_to_html()
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_info_to_html_001(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.life_period = Mock()

        # Mock person methods
        person._give_name_to_html = MagicMock(return_value='first-')
        person._last_name_to_html = MagicMock(return_value='last-')
        person.life_period.to_html = MagicMock(return_value='dates-')
        person._sex_to_html = MagicMock(return_value='sex')

        value = 'first-last-dates-sex'

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._info_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'person-info')
        html_element.set_value.assert_called_once_with(value)

    ##########################################
    # Person._image_to_html()
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_image_to_html_001(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.objects = list()

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._image_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'img')

        expected_calls = [call('class', 'photo'), call('src', 'images/face.png')]
        html_element.add_attribute.mock_calls = expected_calls

    @patch("src.html_element.HTMLElement.__new__")
    def test_image_to_html_001(self, html_element_class):
        # Setup objects
        object1 = Mock()
        object2 = Mock()
        object3 = Mock()
        object1.file = 'path1'
        object2.file = 'path2'
        object3.file = 'path3'

        # Setup persom
        person = Person.__new__(Person)
        person.objects = [object1, object2, object3]

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._image_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'img')

        expected_calls = [call('class', 'photo'), call('src', 'path1')]
        html_element.add_attribute.mock_calls = expected_calls

    ##########################################
    # Person._give_name_to_html()
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_give_name_to_html_001(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.first_name = Mock()

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._give_name_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'first-name')
        html_element.set_value.assert_called_once_with(person.first_name)

    ##########################################
    # Person._last_name_to_html()
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_last_name_to_html_001(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.last_name = Mock()

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._last_name_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'last-name')
        html_element.set_value.assert_called_once_with(person.last_name)

    ##########################################
    # Person._sex_to_html()
    ##########################################

    def test_sex_to_html_001(self):
        # Setup persom
        person = Person.__new__(Person)
        person.sex = ''

        expected = ''
        actual = person._sex_to_html()
        self.assertEqual(expected, actual)

    def test_sex_to_html_002(self):
        # Setup persom
        person = Person.__new__(Person)
        person.sex = 'U'

        expected = ''
        actual = person._sex_to_html()
        self.assertEqual(expected, actual)

    @patch("src.html_element.HTMLElement.__new__")
    def test_sex_to_html_003(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.sex = 'M'

        # Setup html_element
        html_element_to_str = '<div>sex</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._sex_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'img')
        expected_calls = [
            call('class', 'sex'),
            call('src', 'images/sex-M.png'),
            call('alt', 'M')]
        html_element.add_attribute.mock_calls = expected_calls

    @patch("src.html_element.HTMLElement.__new__")
    def test_sex_to_html_004(self, html_element_class):
        # Setup persom
        person = Person.__new__(Person)
        person.sex = 'F'

        # Setup html_element
        html_element_to_str = '<div>sex</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        # Checks
        expected = html_element_to_str
        actual = person._sex_to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'img')
        expected_calls = [
            call('class', 'sex'),
            call('src', 'images/sex-F.png'),
            call('alt', 'F')]
        html_element.add_attribute.mock_calls = expected_calls

    ##########################################
    # Person._split_name
    ##########################################

    def test_split_name_001(self):
        person = Person.__new__(Person)
        full_name = 'First Name /Last Name/'

        split_name = person._split_name(full_name)
        self.assertEqual(split_name, ('First Name', 'Last Name'))

    def test_split_name_002(self):
        person = Person.__new__(Person)
        full_name = '     First Name    /    Last Name   /   '

        split_name = person._split_name(full_name)
        self.assertEqual(split_name, ('First Name', 'Last Name'))

    def test_split_name_003(self):
        person = Person.__new__(Person)
        full_name = '/Last Name/'

        split_name = person._split_name(full_name)
        self.assertEqual(split_name, ('', 'Last Name'))

    def test_split_name_004(self):
        person = Person.__new__(Person)
        full_name = 'First Name //'

        split_name = person._split_name(full_name)
        self.assertEqual(split_name, ('First Name', ''))

    def test_split_name_005(self):
        person = Person.__new__(Person)
        full_name = 'First Name /Last Name'

        split_name = person._split_name(full_name)
        self.assertEqual(split_name, ('First Name', 'Last Name'))

    ##########################################
    # Person.__str__
    ##########################################

    def test_str_001(self):
        person = Person.__new__(Person)
        person.id = "@I1234567@"
        person.first_name = 'First Name'
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
