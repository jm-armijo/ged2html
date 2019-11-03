from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class UnionLinkFormatter():
    def __init__(self, link):
        self.link = link

    def format(self):
        img = HTMLElement('img')
        img.add_attribute('class', 'unionlink-image')
        img.add_attribute('src', 'images/unionlink.png')
        img.add_attribute('id', self.link.id)

        date = self.format_date(self.link.date)

        element = HTMLElement('div', str(img) + date)
        element.add_attribute('class', 'unionlink')

        return str(element)

    def format_date(self, date):
        element = HTMLElement('div')
        element.add_attribute('class', 'person-date')
        element.add_attribute('title', date.get_as_yyyymmdd())
        element.set_value(date.get_year_as_text())
        return str(element)

FormatterFactory.register('UnionLink', UnionLinkFormatter)
