import unittest
from unittest.mock import MagicMock, Mock
from ..object import Object

class TestObject(unittest.TestCase):

    ##########################################
    # Object.__init__
    ##########################################

    def test_init_001(self):
        object_id = '@M12345@'
        object = Object(object_id)

        self.assertEqual(object.id, object_id)
        self.assertEqual(object.file, '')
        self.assertEqual(object.format, '')
        self.assertEqual(object.title, '')

    ##########################################
    # Object.set_file
    ##########################################

    def test_set_file_001(self):
        file = '/path/to/file.ext'

        object = Object.__new__(Object)
        object.set_file(file)
        self.assertEqual(object.file, file)

    ##########################################
    # Object.set_format
    ##########################################

    def test_set_format_001(self):
        format= 'format'

        object = Object.__new__(Object)
        object.set_format(format)
        self.assertEqual(object.format, format)

if __name__ == '__main__':
    unittest.main()
