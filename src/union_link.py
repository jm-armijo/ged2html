from src.date import Date
from src.html import HTMLGenerator

# pylint: disable=too-few-public-methods
class UnionLink():
    def __init__(self, union_id):
        self.id = union_id
        self.date = Date()
        self.place = ''

    def to_html(self):
        value = (
            '    <img class="unionlink-image" src="images/unionlink.png">\n'
            '    {}\n'
        ).format(
            HTMLGenerator.wrap(self.date, self.date.year)
        )

        return HTMLGenerator.wrap(self, value, self.id)
