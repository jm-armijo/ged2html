from src.html_element import HTMLElement

class HTMLDocument():
    def get_document(self):
        head = self._get_head()
        body = self._get_body()
        return self._get_html(head, body)

    def _get_html(self, head, body):
        return (
            '<!doctype html>\n'
            '<html lang="en">\n'
            '{}\n'
            '{}\n'
            '</html>'
        ).format(head, body)

    #################################
    # Head functions
    #################################

    def _get_head(self):
        head_content = self._get_head_meta()
        head_content += self._get_head_icon()
        head_content += self._get_head_title()
        head_content += self._get_head_styles()
        head_content += self._get_head_scripts()

        head = HTMLElement('head')
        head.set_value(head_content)

        return str(head)

    def _get_head_meta(self):
        meta = HTMLElement('meta')
        meta.add_attribute('charset', 'utf-8')
        return str(meta)

    def _get_head_icon(self):
        icon = HTMLElement('link')
        icon.add_attribute('rel', 'icon')
        icon.add_attribute('href', '{}images/icon.png'.format(self.path_to_images))
        return str(icon)

    def _get_head_title(self):
        title = HTMLElement('title')
        title.set_value(self.title.title())
        return str(title)

    def _get_head_styles(self):
        font = HTMLElement('link')
        font.add_attribute('href', "{}css/font_new_rocker.css".format(self.path_to_css))
        font.add_attribute('rel', 'stylesheet')

        css = HTMLElement('link')
        css.add_attribute('href', '{}css/base.css'.format(self.path_to_css))
        css.add_attribute('rel', 'stylesheet')
        return str(font) + str(css)

    def _get_head_scripts(self):
        return ''

    #################################
    # Body functions
    #################################

    def _get_body(self):
        body_content = self._get_body_title()
        body_content += self._get_body_content_wrapper()
        body_content += self._get_body_end_script()

        body = HTMLElement('body')
        body.set_value(body_content)
        return str(body)

    def _get_body_title(self):
        bar = HTMLElement('div')
        bar.add_attribute('class', 'background-bar')
        bar.set_value("&nbsp;")

        title_content = self._get_body_title1()
        title_content += self._get_body_title2()

        title = HTMLElement('div')
        title.add_attribute('class', 'title')
        title.set_value(title_content)

        return str(bar) + str(title)

    def _get_body_content_wrapper(self):
        content = self._get_body_content()

        content_wrapper = HTMLElement('div')
        content_wrapper.add_attribute('class', 'content')
        content_wrapper.set_value(content)

        return str(content_wrapper)

    def _get_body_end_script(self):
        return ''
