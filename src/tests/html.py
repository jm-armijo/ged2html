import unittest
from unittest.mock import MagicMock, Mock, patch, ANY, call
from ..html import HTMLGenerator

class TestHTMLGenerator(unittest.TestCase):

    ##########################################
    # HTMLGenerator.init
    ##########################################

    def test_init_001(self):
        file_name = 'my_tree.ged'
        generator = HTMLGenerator(file_name)
        self.assertEqual(generator.file_name, file_name)

    ##########################################
    # HTMLGenerator.generate
    ##########################################

    @patch("src.html.open", create=True)
    def test_generate_001(self, mock_open):
        # Mock HTMLGenerator methods
        permission = 'w'
        file_name = Mock()
        head = Mock()
        body = Mock()
        html = Mock()

        generator = HTMLGenerator.__new__(HTMLGenerator)
        generator._get_head = MagicMock(return_value = head)
        generator._get_body = MagicMock(return_value = body)
        generator._get_html = MagicMock(return_value = html)
        generator.file_name = file_name

        # Mock file handler
        file_handler = Mock()
        file_handler.write = MagicMock()
        file_handler.close = MagicMock()
        mock_open.return_value = file_handler

        # Calling function to be tested
        title = Mock()
        tree = Mock()
        generator.generate(title, tree)

        # Actual checks
        generator._get_head.assert_called_once_with(title)
        generator._get_body.assert_called_once_with(title, tree)
        generator._get_html.assert_called_once_with(head, body)

        mock_open.assert_called_once_with(file_name, permission)
        file_handler.write.assert_called_once_with(html)
        file_handler.close.assert_called_once_with()

    ##########################################
    # HTMLGenerator.wrap_instance
    ##########################################

    def test_wrap_intance_001(self):
        class_name = 'Mock'
        wrapped_instance = Mock()
        instance = Mock()
        value = Mock()
        attribute_id = ''
        HTMLGenerator.wrap = MagicMock(return_value = wrapped_instance)

        expected = wrapped_instance
        actual = HTMLGenerator.wrap_instance(instance, value)
        self.assertEqual(expected, actual)

        HTMLGenerator.wrap.assert_called_once_with(class_name.lower(), value, attribute_id)

    def test_wrap_intance_002(self):
        class_name = 'Mock'
        wrapped_instance = Mock()
        instance = Mock()
        value = Mock()
        attribute_id = Mock()
        HTMLGenerator.wrap = MagicMock(return_value = wrapped_instance)

        expected = wrapped_instance
        actual = HTMLGenerator.wrap_instance(instance, value, attribute_id)
        self.assertEqual(expected, actual)

        HTMLGenerator.wrap.assert_called_once_with(class_name.lower(), value, attribute_id)

    ##########################################
    # HTMLGenerator.wrap
    ##########################################

    @patch("src.html_element.HTMLElement.__new__")
    def test_wrap_001(self, html_element_class):
        class_name = Mock()
        value = Mock()

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = html_element_to_str
        actual = HTMLGenerator.wrap(class_name, value)
        self.assertEqual(actual, expected)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', class_name)
        html_element.set_value.assert_called_once_with(value)

    @patch("src.html_element.HTMLElement.__new__")
    def test_wrap_002(self, html_element_class):
        class_name = Mock()
        value = Mock()
        attribute_id = ''

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = html_element_to_str
        actual = HTMLGenerator.wrap(class_name, value)
        self.assertEqual(actual, expected, attribute_id)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.add_attribute.assert_called_once_with('class', class_name)
        html_element.set_value.assert_called_once_with(value)

    @patch("src.html_element.HTMLElement.__new__")
    def test_wrap_003(self, html_element_class):
        class_name = Mock()
        value = Mock()
        attribute_id = Mock()

        # Setup html_element
        html_element_to_str = '<div>element</div>'
        html_element = Mock()
        html_element.add_attribute = MagicMock()
        html_element.set_value = MagicMock()
        html_element.__str__ = MagicMock(return_value=html_element_to_str)
        html_element_class.return_value = html_element

        expected = html_element_to_str
        actual = HTMLGenerator.wrap(class_name, value, attribute_id)
        self.assertEqual(actual, expected)

        html_element_class.assert_called_once_with(ANY, 'div')
        html_element.set_value.assert_called_once_with(value)
        mock_calls= [
            call('class', class_name),
            call('id', attribute_id)
        ]
        self.assertEqual(html_element.add_attribute.mock_calls, mock_calls)

    ##########################################
    # HTMLGenerator.list_to_html
    ##########################################

    def test_list_to_html_001(self):
        # Mock list of items
        items = list()
        expected = ''
        actual = HTMLGenerator.list_to_html(items)
        self.assertEqual(expected, actual)

    def test_list_to_html_002(self):
        # Mock list of items
        item1 = Mock()
        item2 = Mock()

        html1 = '<div>X</div>'
        html2 = '<div>Y</div>'
        item1.to_html = MagicMock(return_value = html1)
        item2.to_html = MagicMock(return_value = html2)

        items = [item1, item2]

        expected = html1 + html2
        actual = HTMLGenerator.list_to_html(items)
        self.assertEqual(expected, actual)

    ##########################################
    # HTMLGenerator.get_on_load_script
    ##########################################

    def test_get_on_load_script_001(self):
        script = 'X'
        expected = (
            '  <script>\n'
            '    window.addEventListener(\n'
            '      "load",\n'
            '      function() {\n'
            '        "use strict";\n'
            'X'
            '      }\n'
            '    );\n'
            '  </script>'
        )
        actual = HTMLGenerator.get_on_load_script(script)
        self.assertEqual(expected, actual)

    ##########################################
    # HTMLGenerator._get_html
    ##########################################

    def test_get_html_001(self):
        head = 'X'
        body = 'Y'
        expected = (
            '<!doctype html>\n'
            '<html lang="en">\n'
            'X\n'
            'Y\n'
            '</html>'
        )
        generator = HTMLGenerator.__new__(HTMLGenerator)
        actual = generator._get_html(head, body)
        self.assertEqual(expected, actual)

    ##########################################
    # HTMLGenerator._get_head
    ##########################################

    def test_get_head_001(self):
        title = 'title'
        generator = HTMLGenerator.__new__(HTMLGenerator)

        expected = (
            '  <head>\n'
            '    <meta charset="utf-8">\n'
            '    <title>title</title>\n'
            '    <link href="https://fonts.googleapis.com/css?family=New Rocker" rel="stylesheet">'
            '    <link rel="stylesheet" href="css/styles.css">\n'
            '    <script src="scripts/leader-line.min.js"></script>\n'
            '  </head>'
        )
        actual = generator._get_head(title)
        self.assertEqual(expected, actual)

    def test_get_head_002(self):
        title = ''
        generator = HTMLGenerator.__new__(HTMLGenerator)

        expected = (
            '  <head>\n'
            '    <meta charset="utf-8">\n'
            '    <title></title>\n'
            '    <link href="https://fonts.googleapis.com/css?family=New Rocker" rel="stylesheet">'
            '    <link rel="stylesheet" href="css/styles.css">\n'
            '    <script src="scripts/leader-line.min.js"></script>\n'
            '  </head>'
        )
        actual = generator._get_head(title)
        self.assertEqual(expected, actual)

    ##########################################
    # HTMLGenerator._get_body
    ##########################################

    def test_get_body_001(self):
        title = 'title'
        body = 'body'

        generator = HTMLGenerator.__new__(HTMLGenerator)

        expected = (
            '<body>\n'
            '<div class="title"><h1>title</h1>\n'
            '<h2>Family Tree</h2></div>\n'
            'body\n'
            '</body>'
        )
        actual = generator._get_body(title, body)
        self.assertEqual(expected, actual)

    def test_get_body_002(self):
        title = ''
        body = ''

        generator = HTMLGenerator.__new__(HTMLGenerator)

        expected = (
            '<body>\n'
            '<div class="title"><h1></h1>\n'
            '<h2>Family Tree</h2></div>\n'
            '\n'
            '</body>'
        )
        actual = generator._get_body(title, body)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
