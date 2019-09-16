import unittest
from unittest.mock import  Mock, MagicMock, patch
from ..html import HTMLGenerator
from ..union_link import UnionLink


class TestUnionLink(unittest.TestCase):

    ##########################################
    # UnionLink.__init__
    ##########################################

    @patch("src.date.Date.__new__")
    def test_init_001(self, class_date):
        date = Mock()
        class_date.return_value = date

        union_id = Mock()
        union_link = UnionLink(union_id)

        self.assertEqual(union_link.id, union_id)
        self.assertEqual(union_link.date, date)
        self.assertEqual(union_link.place, '')

    ##########################################
    # UnionLink.to_html
    ##########################################

    def test_to_html_001(self):
        wrapped1 = '<div>date</div>'
        wrapped2 = (
            '<div>\n'
            '    <img class="unionlink-image" src="images/unionlink.png">\n'
            '    {}\n'
            '</div>\n'
        ).format(wrapped1)

        HTMLGenerator.wrap = MagicMock(side_effect = [wrapped1, wrapped2])

        union_link = UnionLink.__new__(UnionLink)
        union_link.id = Mock()
        union_link.date = Mock()

        actual = union_link.to_html()
        expected = wrapped2
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
