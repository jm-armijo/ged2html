from src.element import Element

class File(Element):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.format = ''
        self.title = ''
