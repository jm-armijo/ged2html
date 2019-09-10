import unittest
from unittest.mock import patch
from unittest.mock import Mock

from ..text_line import TextLine

class TestTextLine(unittest.TestCase):

    ##########################################
    # TextLine.init
    ##########################################

    @patch.object(TextLine, 'parse_line')
    def test_init_001(self, mock_req):
        line_str = '0 @IND00032@ INDI'
        line_obj = TextLine(line_str)

        self.assertEqual(line_obj.line, line_str)
        self.assertFalse(hasattr(line_obj, 'level'))
        self.assertFalse(hasattr(line_obj, 'attribute'))
        self.assertFalse(hasattr(line_obj, 'data'))

    ##########################################
    # TextLine.parse_line
    ##########################################

    def test_parse_line_001(self):
        level = 0
        attribute = "@IND00032@"
        data = "INDI"
        line_str = '{} {} {}'.format(level, attribute, data)

        # Creates a raw object of class TextLine
        line_obj = TextLine.__new__(TextLine)

        line_obj.parse_line(line_str)
        self.assertEqual(line_obj.level, level)
        self.assertEqual(line_obj.attribute, attribute)
        self.assertEqual(line_obj.data, data)
        
    def test_parse_line_002(self):
        level = 1845
        attribute = "XYZ"
        data = "A B C D E"
        line_str = '{} {} {}'.format(level, attribute, data)

        # Creates a raw object of class TextLine
        line_obj = TextLine.__new__(TextLine)

        line_obj.parse_line(line_str)
        self.assertEqual(line_obj.level, level)
        self.assertEqual(line_obj.attribute, attribute)
        self.assertEqual(line_obj.data, data)
        
if __name__ == '__main__':
    unittest.main()
