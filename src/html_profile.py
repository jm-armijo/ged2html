from src.html_document import HTMLDocument
from src.html_element import HTMLElement
from src.formatter_person import PersonFormatter

class HTMLProfile(HTMLDocument):
    def __init__(self, title, person):
        self.person = person
        self.path_to_css = '../'
        self.path_to_images = '../'
        self.title = self.person.get_full_name()
        self.formatter = PersonFormatter(person)

    def _get_head_styles(self):
        css = HTMLElement('link')
        css.add_attribute('href', '{}css/profile.css'.format(self.path_to_css))
        css.add_attribute('rel', 'stylesheet')
        return super()._get_head_styles() + str(css)

    def _get_body_title1(self):
        separator = HTMLElement('div')
        separator.add_attribute('class', 'separator')
        separator.set_value(',&nbsp;')

        title = self.formatter.format_last_name()
        title += str(separator)
        title += self.formatter.format_given_name()

        element = HTMLElement('h1')
        element .set_value(title)
        return str(element)

    def _get_body_title2(self):
        value = self.formatter.format_dates_as_title_range()
        element = HTMLElement('h2', value)
        return str(element)

    def _get_body_content(self):
        content  = self._get_body_image()
        content += self.formatter.format_detailed_info()
        content += self.formatter.format_sources()
        return content

    def _get_body_image(self):
        image_html = self.formatter.format_image(self.path_to_css)

        img_wrap = HTMLElement('div', image_html)
        img_wrap.add_attribute('class', 'photo')

        return str(img_wrap)
