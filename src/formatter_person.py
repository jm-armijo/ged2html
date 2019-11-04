import urllib.parse
from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class PersonFormatter():
    def __init__(self, person):
        self.person = person

    def format(self):
        if self.person.is_private():
            person = Person(self.id)
            self.person = person

        value = '{}{}'.format(
            self.format_image(),
            self.format_summary_info()
        )

        element = HTMLElement('a', value)
        element.add_attribute('class', 'person')
        element.add_attribute('id', self.person.id)
        element.add_attribute('href', self.person.id)
        element.add_attribute('target', '_blank')

        return str(element)

    def format_summary_info(self):
        value = '{}{}{}{}'.format(
            self.format_given_name(),
            self.format_last_name(),
            self.format_dates_as_summary_range(),
            self.format_gender_for_tree()
        )

        element = HTMLElement('div', value)
        element.add_attribute('class', 'person-info')
        return str(element)

    def format_detailed_info(self):
        value = '{}{}'.format(
            self.format_detailed_birth_info(),
            self.format_detailed_death_info()
        )

        element = HTMLElement('div', value)
        element.add_attribute('class', 'person-info')
        return str(element)

    def format_image(self, path=''):
        if self.person.objects:
            path += self.person.objects[0].file.path
        else:
            path += 'images/face.png'

        element = HTMLElement('img')
        element.add_attribute('class', 'photo')
        element.add_attribute('src', path)
        return str(element)

    def format_given_name(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'first-name')
        element.set_value(self.person.get_given_name())
        return str(element)

    def format_last_name(self):
        element = HTMLElement('div')
        element.add_attribute('class', 'last-name')
        element.set_value(self.person.get_last_name())
        return str(element)

    def format_gender_for_tree(self):
        value = ''
        if self.person.gender == 'M' or self.person.gender == 'F':
            element = HTMLElement('img')
            element.add_attribute('class', 'sex')
            element.add_attribute('src', 'images/sex-{}.png'.format(self.person.gender))
            element.add_attribute('alt', self.person.gender)
            html = str(element)
        return value

    def format_gender_for_profile(self):
        pass

    def format_detailed_birth_info(self):
        section = ''

        # Date info
        if not self.person.birth.date.is_empty():
            date_value = self.format_detailed_date(self.person.birth.date)
            date_entry = self.format_detailed_info_entry('Date', date_value)
            section += date_entry

        # Place info
        if not self.person.birth.place == '':
            place_value = self.format_place(self.person.birth.place)
            place_entry = self.format_detailed_info_entry('Place', place_value)
            section += place_entry

        return self.format_detailed_section('Birth', section)

    def format_detailed_death_info(self):
        section = ''

        # Date info
        if not self.person.death.date.is_empty():
            date_value = self.format_detailed_date(self.person.death.date)
            date_entry = self.format_detailed_info_entry('Date', date_value)
            section += str(date_entry)

        # Place info
        if not self.person.death.place == '':
            place_value = self.format_place(self.person.death.place)
            place_entry = self.format_detailed_info_entry('Place', place_value)
            section += str(place_entry)

        return self.format_detailed_section('Death', section)

    def format_detailed_section(self, title, content):
        section = ''

        if content != '':
            title = HTMLElement('div', title)
            title.add_attribute('class', 'detailed-info-title')

            section_element = HTMLElement('div', str(title) + content)
            section_element.add_attribute('class', 'detailed-info-section')
        
            section = str(section_element)

        return section

    def format_detailed_info_entry(self, header, value):
        header = self.format_detailed_info_header('{}:'.format(header))

        entry = HTMLElement('div', header + value)
        entry.add_attribute('class', 'detailed-info-entry')
        return str(entry)

    def format_detailed_info_header(self, header):
        header = HTMLElement('div', header)
        header.add_attribute('class', 'detailed-info-header')
        return str(header)

    def format_detailed_date(self, date):
        element = HTMLElement('div', date.get_as_text())
        element.add_attribute('class', 'date')
        return str(element)

    def format_title_date(self, date):
        element = HTMLElement('div', date.get_year_as_text())
        element.add_attribute('class', 'date')
        return str(element)

    def format_summary_date(self, date):
        element = HTMLElement('div', date.get_year_as_text())
        element.add_attribute('class', 'date')
        element.add_attribute('title', date.get_as_yyyymmdd())
        return str(element)

    def format_place(self, place):
        if place == '':
            return ''

        query = urllib.parse.quote(place)
        url = "https://www.google.com/maps/search/?api=1&query={}".format(query)

        element = HTMLElement('a', place)
        element.add_attribute('class', 'place')
        element.add_attribute('href', url)
        element.add_attribute('target', '_blank')
        return str(element)

    def format_sources(self):
        sources = ''
        for source in self.person.get_sources():
            formatter = FormatterFactory.make(source)
            sources += formatter.format()

        element = HTMLElement('div', sources)
        element.add_attribute('class', 'sources')

        return str(element)

    def format_dates_as_title_range(self):
        dates = ''
        if self.person.can_show_dates():
            separator = HTMLElement('div', '&ndash;')
            separator.add_attribute('class', 'separator')

            dates = self.format_title_date(self.person.birth.date)
            dates += str(separator)
            dates += self.format_title_date(self.person.death.date)

        element = HTMLElement('div', dates)
        element.add_attribute('class', 'date-range')

        return str(element)

    def format_dates_as_summary_range(self):
        dates = ''
        if self.person.can_show_dates():
            separator = HTMLElement('div', '&ndash;')
            separator.add_attribute('class', 'separator')

            dates = self.format_summary_date(self.person.birth.date)
            dates += str(separator)
            dates += self.format_summary_date(self.person.death.date)

        element = HTMLElement('div', dates)
        element.add_attribute('class', 'date-range')

        return str(element)

FormatterFactory.register('Person', PersonFormatter)
