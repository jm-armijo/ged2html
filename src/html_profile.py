from src.html_document import HTMLDocument
from src.html_element import HTMLElement

class HTMLProfile(HTMLDocument):
    def __init__(self, title, person):
        self.path_to_css = '../'
        self.path_to_images = '../'
        self.person = person
        self.title = self.person.get_full_name()

    def _get_head_styles(self):
        css = HTMLElement('link')
        css.add_attribute('href', '{}css/profile.css'.format(self.path_to_css))
        css.add_attribute('rel', 'stylesheet')
        return super()._get_head_styles() + str(css)

    def _get_body_title1(self):
        separator = HTMLElement('div')
        separator.add_attribute('class', 'separator')
        separator.set_value(',&nbsp;')

        title = self.person.last_name_to_html()
        title += str(separator)
        title += self.person.first_name_to_html()

        element = HTMLElement('h1')
        element .set_value(title)
        return str(element)

    def _get_body_title2(self):
        value = self.person.get_date_range()
        element = HTMLElement('h2')
        element .set_value(value)
        return str(element)

    def _get_body_content(self):
        content  = self._get_body_image()
        content += self._get_body_info()
        content += self._get_body_sources()
        return content

    def _get_body_sources(self):
        sources_content = self.person.sources_to_html()

        sources = HTMLElement('div')
        sources.add_attribute('class', 'sources')
        sources.set_value(sources_content)

        return str(sources)

    def _get_body_info(self):
        content = self._get_birth_info()
        content += self._get_death_info()

        info = HTMLElement('div')
        info.add_attribute('class', 'person-info')
        info.set_value(content)

        return str(info)

    def _get_body_image(self):
        image_html = self.person.image_to_html(self.path_to_css)

        img_wrap = HTMLElement('div')
        img_wrap.add_attribute('class', 'photo')
        img_wrap.set_value(image_html)

        return str(img_wrap)

    def _get_birth_info(self):
        name = self.person.first_name.title()
        place = self.person.birth_place_to_html()
        date = self.person.get_birth_date().get_as_text()

        if place == '' and date == '':
            return ''

        text  = "{} was born ".format(name)

        if place != '':
            text += " in {}".format(place)

        if date != '':
            text += " on {}".format(date)

        element = HTMLElement('div')
        element.add_attribute('class', 'text')
        element.set_value(text)

        return str(element)

    def _get_death_info(self):
        pronoun = self.person.get_pronoun().title()
        place = self.person.death_place_to_html()
        date = self.person.get_death_date().get_as_text()

        if place == '' and date == '':
            return ''

        text  = "{} died ".format(pronoun)

        if place != '':
            text += " in {}".format(place)

        if date != '':
            text += " on {}".format(date)

        element = HTMLElement('div')
        element.add_attribute('class', 'text')
        element.set_value(text)

        return str(element)

    def _get_sex(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'sex')
        element.set_value("Sex : {}".format(self.person.sex))
        return str(element)
