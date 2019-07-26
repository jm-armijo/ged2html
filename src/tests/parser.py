import unittest
from unittest.mock import patch
from unittest.mock import Mock
from ..parser import Parser

def parseLine():
	return M

class TestParser(unittest.TestCase):
	def test_init_001(self):
		parser = Parser()
		self.assertEqual(len(parser.people),0)
		self.assertIsNone(parser.current_line)
		self.assertEqual(parser.state, 'IDLE')

	@patch.object(Parser, 'getCurrentState')
	@patch.object(Parser, 'parseCurrentLine')
	def test_parse_lines_001(self, mock_parse, mock_get):
		# Setup
		lines = [Mock(), Mock(), Mock()]
		parser_obj = Parser.__new__(Parser)
		parser_obj.people = list()

		# Actual test
		people = parser_obj.parseLines(lines)
		self.assertTrue(mock_get.called)
		self.assertTrue(mock_parse.called)
		self.assertEqual(people, parser_obj.people)

		#self.assertEqual(mock_get.called_count, len(lines))
		#self.assertEqual(mock_parse.called_count, len(lines))

	# STATE MACHINE TESTS

	# From any state goes to INDI when level = 0
	def test_get_current_state_001(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI')

	# From any state goes to FAM when level = 0
	def test_get_current_state_002(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Current state left undefined, as value is not used.
		# level and data values must be as below
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'FAM'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM')

	# Stays on IDLE if level > 0
	def test_get_current_state_003(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'IDLE'
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From FAM goes to IDLE if no more data
	def test_get_current_state_004(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'FAM'
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to IDLE if no more data
	def test_get_current_state_005(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.current_line = Mock()

		# Line data left undefined, as value is not used.
		parser_obj.state = 'INDI'
		parser_obj.current_line.level = 0
		parser_obj.current_line.data = 'Any value but FAM or INDI'

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'IDLE')

	# From INDI goes to INDI_DATA (level 1)
	def test_get_current_state_006(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI goes to INDI_DATA (level 9999)
	def test_get_current_state_007(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 1)
	def test_get_current_state_008(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From INDI_DATA goes to INDI_DATA (level 9999)
	def test_get_current_state_009(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'INDI_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'INDI_DATA')

	# From FAM goes to FAM_DATA (level 1)
	def test_get_current_state_010(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM goes to FAM_DATA (level 9999)
	def test_get_current_state_011(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM'

		# Line data left undefined, as value is not used.
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 1)
	def test_get_current_state_012(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 1

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

	# From FAM_DATA goes to FAM_DATA (level 9999)
	def test_get_current_state_013(self):
		# Setup
		parser_obj = Parser.__new__(Parser)
		parser_obj.state = 'FAM_DATA'
		parser_obj.current_line = Mock()
		parser_obj.current_line.level = 9999

		# Actual test
		new_state = parser_obj.getCurrentState()
		self.assertEqual(new_state, 'FAM_DATA')

if __name__ == '__main__':
	unittest.main()
