from src.html import HTMLGenerator

class TreeLevel():
    def __init__(self):
        self.nodes = list()

    def append(self, node):
        self.nodes.append(node)

    def to_html(self):
        value = HTMLGenerator.list_to_html(self.nodes)
        return HTMLGenerator.wrap(self, value)
