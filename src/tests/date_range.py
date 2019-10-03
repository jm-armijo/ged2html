import unittest
from unittest.mock import MagicMock, Mock, patch, ANY, call
from ..date_range import DateRange
from ..html import HTMLGenerator

class TestDateRange(unittest.TestCase):

    ##########################################
    # DateRange.init
    ##########################################

    @patch("src.date.Date.__new__")
    def test_init_001(self, class_date):
        start_date = Mock()
        end_date = Mock()
        class_date.side_effect = [start_date, end_date]

        date_range = DateRange()
        self.assertEqual(start_date, date_range.start)
        self.assertEqual(end_date, date_range.end)

    ##########################################
    # DateRange.to_html
    ##########################################

    def test_to_html_001(self):
        # Setup date_range
        date_range = DateRange.__new__(DateRange)
        date_range.start = Mock()
        date_range.end = Mock()
        date_range.start.is_empty = MagicMock(return_value=True)
        date_range.end.is_empty = MagicMock(return_value=True)
        date_range.start.to_html = MagicMock(return_value='')
        date_range.end.to_html = MagicMock(return_value='')

        expected = ''
        actual = date_range.to_html()
        self.assertEqual(expected, actual)

    @patch("src.html_element.HTMLElement.__new__")
    def test_to_html_002(self, html_element_class):
        # Setup date_range
        date_range = DateRange.__new__(DateRange)
        date_range.start = Mock()
        date_range.end = Mock()
        date_range.start.is_empty = MagicMock(return_value=False)
        date_range.end.is_empty = MagicMock(return_value=True)
        date_range.start.to_html = MagicMock(return_value='start')
        date_range.end.to_html = MagicMock(return_value='')

        # Setup html_element
        html_element_to_str = '-'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = 'start-'
        actual = date_range.to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'separator')
        html_element.set_value.assert_called_once_with('&ndash;')

    @patch("src.html_element.HTMLElement.__new__")
    def test_to_html_003(self, html_element_class):
        # Setup date_range
        date_range = DateRange.__new__(DateRange)
        date_range.start = Mock()
        date_range.end = Mock()
        date_range.start.is_empty = MagicMock(return_value=True)
        date_range.end.is_empty = MagicMock(return_value=False)
        date_range.start.to_html = MagicMock(return_value='')
        date_range.end.to_html = MagicMock(return_value='end')

        # Setup html_element
        html_element_to_str = '-'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = '-end'
        actual = date_range.to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'separator')
        html_element.set_value.assert_called_once_with('&ndash;')

    @patch("src.html_element.HTMLElement.__new__")
    def test_to_html_004(self, html_element_class):
        # Setup date_range
        date_range = DateRange.__new__(DateRange)
        date_range.start = Mock()
        date_range.end = Mock()
        date_range.start.is_empty = MagicMock(return_value=False)
        date_range.end.is_empty = MagicMock(return_value=False)
        date_range.start.to_html = MagicMock(return_value='start')
        date_range.end.to_html = MagicMock(return_value='end')

        # Setup html_element
        html_element_to_str = '-'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = 'start-end'
        actual = date_range.to_html()
        self.assertEqual(expected, actual)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', 'separator')
        html_element.set_value.assert_called_once_with('&ndash;')

if __name__ == '__main__':
    unittest.main()
