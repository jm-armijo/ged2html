from src.date import Date
from src.html_element import HTMLElement

# pylint: disable=too-few-public-methods
class UnionLink():
    def __init__(self, union_id):
        self.id = union_id
        self.date = Date()
        self.place = ''

    def is_private(self):
        return True

    def to_html(self):
        value = (
            '    <img class="unionlink-image" src="images/unionlink.png" id={}>\n'
            '    {}\n'
        ).format(
            self.id,
            self.date.to_html()
        )

        link = HTMLElement('div')
        link.add_attribute('class', 'unionlink')
        link.set_value(value)

        return str(link)
