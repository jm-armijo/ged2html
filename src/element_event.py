from src.date import Date
from src.element import Element

class Event(Element):
    def __init__(self, type=''):
        super().__init__()
        self.type = type
        self.place = ''
        self.date = Date()
