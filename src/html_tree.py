from src.html_document import HTMLDocument
from src.html_element import HTMLElement
from src.formatter_factory import FormatterFactory

class HTMLTree(HTMLDocument):
    def __init__(self, title, tree):
        self.path_to_css = ''
        self.path_to_images = ''
        self.tree = tree
        self.title = title

    def _get_head_styles(self):
        css = HTMLElement('link')
        css.add_attribute('href', '{}css/tree.css'.format(self.path_to_css))
        css.add_attribute('rel', 'stylesheet')
        return super()._get_head_styles() + str(css)

    def _get_head_scripts(self):
        script = HTMLElement('script')
        script.add_attribute('src', 'scripts/leader-line.min.js')
        return str(script)

    ######## STRUCTURE OF HTML BODY ############
    #
    #  +-body-----------------------------+
    #  |                                  |
    #  |  +-title----------------------+  |
    #  |  |                            |  |
    #  |  +----------------------------+  |
    #  |                                  |
    #  |  +-content--------------------+  |
    #  |  |                            |  |
    #  |  |  +-level-----------------+ |  |
    #  |  |  |                       | |  |
    #  |  |  |  [node] [node] [node] | |  |
    #  |  |  +-----------------------+ |  |
    #  |  +----------------------------+  |
    #  +----------------------------------+
    #
    ############################################

    def _get_body_title1(self):
        h1 = HTMLElement('h1')
        h1.set_value(self.title)
        return str(h1)

    def _get_body_title2(self):
        h2 = HTMLElement('h2')
        h2.set_value('Family Tree')
        return str(h2)

    def _get_body_content(self):
        content = ''
        for level in self.tree.nodes:
            content += self._get_tree_level(level)
        return content

    def _get_tree_level(self, level):
        nodes = ''
        for node in level.nodes:
            nodes += self._get_tree_node(node)

        element = HTMLElement('div')
        element.add_attribute('class', 'treelevel')
        element.set_value(nodes)
        return str(element)

    def _get_tree_node(self, node):
        if node.node.is_private():
            return ''

        formatter = FormatterFactory.make(node.node)

        element = HTMLElement('div', formatter.format())
        element.add_attribute('class', 'treenode')

        return str(element)

    def _get_body_end_script(self):
        event_listener = self._get_event_listener_script()
        script = HTMLElement('script')
        script.set_value(event_listener)
        return str(script)

    def _get_event_listener_script(self):
        edges_script = ''
        for edge in self.tree.edges:
            edges_script += self._get_edge_script(edge)

        return (
            '    window.addEventListener(\n'
            '      "load",\n'
            '      function() {{\n'
            '        "use strict";\n'
            '{}'
            '      }}\n'
            '    );\n'
        ).format(edges_script)

    def _get_edge_script(self, edge):
        return (
            '        new LeaderLine(\n'
            '          document.getElementById("{}"),\n'
            '          document.getElementById("{}"),\n'
            '          {{'
            '            color: "White", '
            '            startSocket: "top", '
            '            endSocket: "bottom", '
            '            path: "magnet", '
            '            size: 2, '
            '            startPlug: "disc", '
            '            endPlug: "disc"'
            '          }}\n'
            '        );\n'
        ).format(edge.start, edge.end)
