from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class UnionFormatter():
    def __init__(self, union):
        self.union = union

    def format(self):
        img = HTMLElement('img')
        img.add_attribute('class', 'unionlink-image')
        img.add_attribute('src', 'images/unionlink.png')
        img.add_attribute('id', self.union.id)

        date = ''
        if self.union.spouse1.is_dead() and self.union.spouse2.is_dead():
            date = self.format_date(self.union.marriage.date)

        element = HTMLElement('div', str(img) + date)
        element.add_attribute('class', 'unionlink')

        return str(element)

    def format_date(self, date):
        element = HTMLElement('div')
        element.add_attribute('class', 'person-date')
        element.add_attribute('title', date.get_as_yyyymmdd())
        element.set_value(date.get_year_as_text())
        return str(element)

FormatterFactory.register('Union', UnionFormatter)
