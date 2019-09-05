import unittest
from unittest.mock import Mock, MagicMock
from ..edge import Edge

class TestEdge(unittest.TestCase):

    ##########################################
    # Edge.__init__
    ##########################################

    def test_init_001(self):
        start = Mock()
        end = Mock()
        edge = Edge(start, end)
        self.assertEqual(edge.start, start)
        self.assertEqual(edge.end, end)

    ##########################################
    # Edge.to_html
    ##########################################

    def test_init_001(self):
        start = 'X'
        end = 'Y'

        expected = (
            '        new LeaderLine(\n'
            '          document.getElementById("X"),\n'
            '          document.getElementById("Y"),\n'
            '          {startSocket: "top", endSocket: "bottom", path: "magnet"}\n'
            '        );\n'
        )

        edge = Edge.__new__(Edge)
        edge.start = start
        edge.end = end

        actual = edge.to_html()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
