from src.node import Node

class NullPerson(Node):
    # pylint: disable=no-self-use
    def to_html(self):
        return '<div class="person"></div>'

    # pylint: disable=no-self-use
    def get_unions(self):
        return list()
