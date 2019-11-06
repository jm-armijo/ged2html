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
        value = '{}{}{}{}{}{}{}{}'.format(
            self.format_detailed_birth_info(),
            self.format_detailed_gender_info(),
            self.format_detailed_nationality_info(),
            self.format_detailed_baptism_info(),
            self.format_detailed_occupation_info(),
            self.format_detailed_marriages_info(),
            self.format_detailed_death_info(),
            self.format_detailed_burial_info()
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

    def format_detailed_nationality_info(self):
        section = self.format_detailed_event(self.person.nationality)
        return self.format_detailed_section('Nationality', section)

    def format_detailed_occupation_info(self):
        section = self.format_detailed_event(self.person.occupation)
        return self.format_detailed_section('Occupation', section)

    def format_detailed_gender_info(self):
        section = ''
        if self.person.gender:
            entry = HTMLElement('div', self.person.gender)
            entry.add_attribute('class', 'detailed-info-entry')
            section += str(entry)
        return self.format_detailed_section('Gender', section)

    def format_detailed_birth_info(self):
        section = self.format_detailed_event(self.person.birth)
        return self.format_detailed_section('Birth', section)

    def format_detailed_baptism_info(self):
        section = self.format_detailed_event(self.person.baptism)
        return self.format_detailed_section('Baptism', section)

    def format_detailed_marriages_info(self):
        marriages = ''
        for union in self.person.unions:
            marriages += self.format_detailed_marriage_info(union)
        return marriages

    def format_detailed_marriage_info(self, union):
        section = self.format_detailed_event(union.marriage)
        section += self.format_spouse_name(union)
        return self.format_detailed_section('Marriage', section)

    def format_spouse_name(self, union):
        header = self.format_detailed_info_header('{}:'.format('Spouse'))
        spouse = union.get_other_spouse(self.person)
        name = spouse.name.get_full().title()
        entry = HTMLElement('div', header + name)
        entry.add_attribute('class', 'detailed-info-entry')
        return str(entry)

    def format_detailed_death_info(self):
        section = self.format_detailed_event(self.person.death)
        return self.format_detailed_section('Death', section)

    def format_detailed_burial_info(self):
        section = self.format_detailed_event(self.person.burial)
        return self.format_detailed_section('Burial', section)

    def format_detailed_event(self, event):
        section = ''

        if event.type:
            entry = HTMLElement('div', event.type)
            entry.add_attribute('class', 'detailed-info-entry')
            section += str(entry)

        # Date info
        if not event.date.is_empty():
            date_value = self.format_detailed_date(event.date)
            date_entry = self.format_detailed_info_entry('Date', date_value)
            section += date_entry

        # Place info
        if event.place:
            place_value = self.format_place(event.place)
            place_entry = self.format_detailed_info_entry('Place', place_value)
            section += place_entry

        sources = self.format_sources(event)
        if sources:
            sources_entry = self.format_detailed_info_entry('Sources', sources)
            section += sources_entry

        return section

    def format_sources(self, event):
        sources = list()
        for source in event.sources:
            sources += self.format_source(source)

        return ', '.join(sources)

    def format_source(self, source):
        formatted_source = list()
        formatter = FormatterFactory.make(source)
        source = formatter.format()

        if source != '':
            formatted_source.append(source)

        return formatted_source

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
