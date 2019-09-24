import unittest
from unittest.mock import Mock, MagicMock, patch, ANY, call
from ..date import Date

class TestDate(unittest.TestCase):

    ##########################################
    # Date.init
    ##########################################

    def test_init_001(self):
        date = Date()

        self.assertEqual(date.precision, '')
        self.assertEqual(date.day, '')
        self.assertEqual(date.month, '')
        self.assertEqual(date.year, '')

    ##########################################
    # Date.is_empty
    ##########################################

    def test_is_empty_001(self):
        date = Date.__new__(Date)
        date.year = ''

        actual = date.is_empty()
        self.assertEqual(True, actual)

    def test_is_empty_002(self):
        date = Date.__new__(Date)
        date.year = 'x'

        actual = date.is_empty()
        self.assertEqual(False, actual)

    def test_is_empty_003(self):
        date = Date.__new__(Date)
        date.year = None

        actual = date.is_empty()
        self.assertEqual(False, actual)

    ##########################################
    # Date.set_precision
    ##########################################

    def test_set_precision_001(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = ''

        precision = 'ABT'
        date.set_precision(precision)
        self.assertEqual(date.precision, precision)
        self.assertEqual(date.day, '')
        self.assertEqual(date.month, '')
        self.assertEqual(date.year, '')

    ##########################################
    # Date.set_day
    ##########################################

    def test_set_day_001(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = ''

        day = '9'
        date.set_day(day)
        self.assertEqual(date.precision, '')
        self.assertEqual(date.day, day)
        self.assertEqual(date.month, '')
        self.assertEqual(date.year, '')

    ##########################################
    # Date.set_month
    ##########################################

    def test_set_month_001(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = ''

        month = 'AUG'
        date.set_month(month)
        self.assertEqual(date.precision, '')
        self.assertEqual(date.day, '')
        self.assertEqual(date.month, month)
        self.assertEqual(date.year, '')

    ##########################################
    # Date.set_year
    ##########################################

    def test_set_year_001(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = ''

        year = '1865'
        date.set_year(year)
        self.assertEqual(date.precision, '')
        self.assertEqual(date.day, '')
        self.assertEqual(date.month, '')
        self.assertEqual(date.year, year)

    ##########################################
    # Date.to_html
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_to_html_001(self, html_element_class):
        date = Date.__new__(Date)
        date.year = 'year'
        date._get_full = MagicMock(return_value='full-date')

        # Setup html_element
        html_element_to_str = 'element'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = 'element'
        actual = date.to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        calls = [
            call('class', 'person-date'),
            call('title', 'full-date')
        ]
        self.assertEqual(html_element.add_attribute.mock_calls, calls)
        html_element.set_value.assert_called_once_with('year')

    ##########################################
    # Date._get_full
    ##########################################

    def test_get_full_001(self):
        date = Date.__new__(Date)
        date.precision = 'EST'
        date.day = '14'
        date.month = 'APR'
        date.year = '1899'

        current = date._get_full()
        self.assertEqual(current, '14 APR 1899')

    def test_get_full_002(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = '14'
        date.month = 'APR'
        date.year = '1899'

        current = date._get_full()
        self.assertEqual(current, '14 APR 1899')

    def test_get_full_003(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = 'APR'
        date.year = '1899'

        current = date._get_full()
        self.assertEqual(current, 'APR 1899')

    def test_get_full_004(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = '1899'

        current = date._get_full()
        self.assertEqual(current, '1899')

if __name__ == '__main__':
    unittest.main()
