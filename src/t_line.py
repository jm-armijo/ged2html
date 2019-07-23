import unittest
from unittest.mock import patch
from unittest.mock import Mock
from line import Line

class TestLine(unittest.TestCase):
	@patch.object(Line, 'parseLine')
	def test_init_001(self, mock_req):
		line_str = '0 @IND00032@ INDI'
		line_obj = Line(line_str)

		self.assertEqual(line_obj.line, line_str)
		self.assertFalse(hasattr(line_obj, 'level'))
		self.assertFalse(hasattr(line_obj, 'attribute'))
		self.assertFalse(hasattr(line_obj, 'data'))

	def test_parse_line_001(self):
		level = 0
		attribute = "@IND00032@"
		data = "INDI"
		line_str = '{} {} {}'.format(level, attribute, data)

		# Creates a raw object of class Line
		line_obj = Line.__new__(Line)

		line_obj.parseLine(line_str)
		self.assertEqual(line_obj.level, level)
		self.assertEqual(line_obj.attribute, attribute)
		self.assertEqual(line_obj.data, data)
		
	def test_parse_line_002(self):
		level = 1845
		attribute = "XYZ"
		data = "A B C D E"
		line_str = '{} {} {}'.format(level, attribute, data)

		# Creates a raw object of class Line
		line_obj = Line.__new__(Line)

		line_obj.parseLine(line_str)
		self.assertEqual(line_obj.level, level)
		self.assertEqual(line_obj.attribute, attribute)
		self.assertEqual(line_obj.data, data)
		
	#def test_is_person_header_001(self):
	#	# Creates a raw object of class Line
	#	line_obj = Line.__new__(Line)
	#	line_obj.level = '0'
	#	line_obj.data = "INDI"

	#	self.assertTrue(line_obj.isPersonHeader())

	#def test_is_person_header_002(self):
	#	# Creates a raw object of class Line
	#	line_obj = Line.__new__(Line)
	#	line_obj.level = '1'
	#	line_obj.data = "INDI"

	#	self.assertFalse(line_obj.isPersonHeader())

	#def test_is_person_header_003(self):
	#	# Creates a raw object of class Line
	#	line_obj = Line.__new__(Line)
	#	line_obj.level = '0'
	#	line_obj.data = "XYZ"

	#	self.assertFalse(line_obj.isPersonHeader())

	#def test_is_person_header_004(self):
	#	# Creates a raw object of class Line
	#	line_obj = Line.__new__(Line)
	#	line_obj.level = '1'
	#	line_obj.data = "XYZ"

	#	self.assertFalse(line_obj.isPersonHeader())

if __name__ == '__main__':
	unittest.main()
