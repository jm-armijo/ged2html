import unittest
from unittest.mock import Mock, MagicMock, patch, ANY, call
from ..html_element import HTMLElement

class TestDate(unittest.TestCase):

    ##########################################
    # HTMLElement.init
    ##########################################

    def test_init_001(self):
        tag = Mock()
        html_element = HTMLElement(tag)
        self.assertEqual(html_element.tag, tag)
        self.assertEqual(html_element.attributes, dict())
        self.assertEqual(html_element.value, None)

    ##########################################
    # HTMLElement.add_attribute
    ##########################################

    def test_add_attribute_001(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.attributes = dict()

        attr_name = Mock()
        attr_val = Mock()
        html_element.add_attribute(attr_name, attr_val)

        self.assertEqual(html_element.attributes[attr_name], attr_val)

    def test_add_attribute_002(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.attributes = dict()

        attr_name = Mock()
        attr_val1 = Mock()
        attr_val2 = Mock()
        html_element.add_attribute(attr_name, attr_val1)
        html_element.add_attribute(attr_name, attr_val2)

        self.assertEqual(html_element.attributes[attr_name], attr_val2)

    ##########################################
    # HTMLElement.set_value
    ##########################################

    def test_set_value_001(self):
        html_element = HTMLElement.__new__(HTMLElement)
        value = Mock()
        html_element.set_value(value)

        self.assertEqual(html_element.value, value)

    ##########################################
    # HTMLElement.__str__
    ##########################################

    def test_str_001(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.tag = 'x'
        html_element.attributes = dict()
        html_element.value = None

        expected = '<x/>'
        actual = html_element.__str__()
        self.assertEqual(expected, actual)

    def test_str_002(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.tag = 'x'
        html_element.attributes = dict()
        html_element.value = 'y'

        expected = '<x>y</x>'
        actual = html_element.__str__()
        self.assertEqual(expected, actual)

    def test_str_003(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.tag = 'x'
        html_element.attributes = {'k1': 'v1'}
        html_element.value = 'y'

        expected = '<x k1="v1">y</x>'
        actual = html_element.__str__()
        self.assertEqual(expected, actual)

    def test_str_004(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.tag = 'x'
        html_element.attributes = {'k1': 'v1', 'k2': 'v2'}
        html_element.value = 'y'

        expected = '<x k1="v1" k2="v2">y</x>'
        actual = html_element.__str__()
        self.assertEqual(expected, actual)

    def test_str_005(self):
        html_element = HTMLElement.__new__(HTMLElement)
        html_element.tag = 'x'
        html_element.attributes = {'k1': 'v1', 'k2': 'v2'}
        html_element.value = None

        expected = '<x k1="v1" k2="v2"/>'
        actual = html_element.__str__()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
