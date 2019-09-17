import unittest
from unittest.mock import Mock, MagicMock
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
    # Date.get_full
    ##########################################

    def test_get_full_001(self):
        date = Date.__new__(Date)
        date.precision = 'EST'
        date.day = '14'
        date.month = 'APR'
        date.year = '1899'

        current = date.get_full()
        self.assertEqual(current, '14 APR 1899')

    def test_get_full_002(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = '14'
        date.month = 'APR'
        date.year = '1899'

        current = date.get_full()
        self.assertEqual(current, '14 APR 1899')

    def test_get_full_003(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = 'APR'
        date.year = '1899'

        current = date.get_full()
        self.assertEqual(current, 'APR 1899')

    def test_get_full_004(self):
        date = Date.__new__(Date)
        date.precision = ''
        date.day = ''
        date.month = ''
        date.year = '1899'

        current = date.get_full()
        self.assertEqual(current, '1899')

if __name__ == '__main__':
    unittest.main()
