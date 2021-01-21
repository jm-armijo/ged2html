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
        body_content = self._get_top_bar()
        body_content += self._get_body_content_wrapper()
        body_content += self._get_body_end_script()

        body = HTMLElement('body')
        body.set_value(body_content)
        return str(body)

    def _get_top_bar(self):
        padding_bar = self._get_padding_bar()
        home_logo = self._get_home_logo()
        title = self._get_body_title()

        bar = HTMLElement('div')
        bar.add_attribute('class', 'top-bar')
        bar.set_value(padding_bar + home_logo + title)

        return str(bar)

    def _get_padding_bar(self):
        bar = HTMLElement('div')
        bar.add_attribute('class', 'background-bar')
        bar.set_value("&nbsp;")

        return str(bar)

    def _get_home_logo(self):
        home_img = HTMLElement('img')
        home_img.add_attribute('class', 'home-logo')
        home_img.add_attribute('src', "{}images/tree.png".format(self.path_to_images))

        home_link = HTMLElement('a')
        home_link.add_attribute('class', 'home-logo')
        home_link.add_attribute('href', "/family")
        home_link.set_value(str(home_img))

        home_div = HTMLElement('div')
        home_div.add_attribute('class', 'home-logo')
        home_div.set_value(str(home_link))

        return str(home_div)

    def _get_body_title(self):
        title_content  = self._get_body_title1()
        title_content += self._get_body_title2()

        title = HTMLElement('div')
        title.add_attribute('class', 'title')
        title.set_value(title_content)

        return str(title)

    def _get_body_content_wrapper(self):
        content = self._get_body_content()

        content_wrapper = HTMLElement('div')
        content_wrapper.add_attribute('class', 'content')
        content_wrapper.set_value(content)

        return str(content_wrapper)

    def _get_body_end_script(self):
        return ''
