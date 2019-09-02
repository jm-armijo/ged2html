from src.html import HTMLGenerator

# pylint: disable=too-few-public-methods
class TreeNode():
    def __init__(self, node):
        self.node = node

    def to_html(self):
        value = self.node.to_html()
        return HTMLGenerator.wrap(self, value)
